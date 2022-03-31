from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .forms import TickerForm, AssetForm, HoldingForm
from .models import Asset
from django.template.loader import render_to_string
from django.db import IntegrityError
import json


import yfinance as yf
# Create your views here.

#figure out session_exists true false changing how Im using it
# i need it for session storage
# if a user has searched already
# start,save session of validate form so its not blank?

# if request get
# access asset
#session['ticker'] = ticker
#within get I can check if it exists or not
##if it does then asset = something otherwise something for context
##Do I need context for post?
##save session info at post and ask from there at get


class StartingPageView(View):
    def get(self, request):
        ##searched already
        # if request.session.get('error_exists'):
        #     context ={
        #         "errExists": True,
        #         'message':  request.session.get('message'),
        #         "ticker_form":TickerForm()
        #     }
        #     request.session['error_exists'] = False
        #     request.session['message'] = ''
        #     # render(request, 'portfolioapp/index.html', context)  
        # else:
            if request.session.get('session_exists'): 
                ticker_input = request.session.get('ticker_input')
                ticker_asset = yf.Ticker(ticker_input)
                info = ticker_asset.info
            #invalid ticker
                if info["regularMarketPrice"] == None:
                    # set valid ticker identifier False
                    ticker_valid = False
                    # error exists that ticker doesnt exist
                    request.session['error_exists'] = True
                    request.session['message'] = 'Asset doesnot exist. Please try another ticker'
                    context = {
                    "ticker_form":TickerForm(),
                    'ticker_valid': ticker_valid,
                    "message": request.session.get('message')
                    }
            #valid ticker   
                else:
                    # set valid identifier True  
                    ticker_valid = True 
                    # switch session exists to False otherwse it will show current data at refresh
                    request.session['session_exists'] = False
                    request.session['ticker_name'] = ticker_input 
                    # no error
                    request.session['error_exists'] = False
                    holdings = Asset.objects.filter(ticker= ticker_input, session = self.request.session.session_key)
                    if len(holdings) > 0:
                        btn_action = 'exists'
                    else:
                        btn_action = 'add'
                    # form to accept ticker name, pp, pq
                    context = {
                    "ticker_form":TickerForm(),
                    "ticker_valid": ticker_valid,
                    "asset_ticker": request.session['ticker_name'],
                    "asset_name": ticker_asset.info['shortName'],
                    "news": ticker_asset.news,
                    "message": request.session.get('message'),
                    "btn_action": btn_action
                    } 
                    request.session['message'] = ''
            else:
                # at load - search hasnt started yet
                ticker_valid = False
                context = {
                "ticker_form":TickerForm(),
                'ticker_valid': ticker_valid,
                "news": ""
                }
            return render(request, 'portfolioapp/index.html', context)

    def post(self, request):
        #if search button is clicked
        # if 'searchticker' in request.POST:
        ticker_form = TickerForm(request.POST)
    #form isnt blank
        if ticker_form.is_valid():
            ticker_input = ticker_form.cleaned_data['ticker'].upper()
            request.session['ticker_input'] = ticker_input
            request.session['session_exists'] = True
            request.session['error_exists'] = False
            request.session['message'] = ''
        #form is blank
        else:
            request.session['message'] = "form is blank"
            request.session['session_exists'] = False
        return HttpResponseRedirect(reverse('starting-page'))
                      
class PortfolioPageView(View):
    def get(self, request):
        # retrieve users portfolio
        holdings = Asset.objects.filter(session = self.request.session.session_key)
        return_doll = 0
        sum_net = 0 
        ppTot = 0
        # calculate total return and return per asset in portfolio 
        for holding in holdings:
            ticker_asset = yf.Ticker(holding.ticker)
            holding.closing_price = round(ticker_asset.history(period="1d").iloc[0]["Close"])
            # for each asset get purchase_price, purchase_quantity, closing price
            # if price, quantity not added previously assign 0
            if holding.purchase_price:
                pp = holding.purchase_price
                pq = holding.purchase_quantity
                cp = holding.closing_price    
                holding.total_return = round(cp*pq)
                holding.net_return = round((cp-pp)*pq)
            else: 
                pp = 0
                pq = 0
                cp = 0
            return_doll += (cp - pp)*pq
            sum_net += (cp - pp)
            ppTot += pp
        if ppTot > 0:
            return_per = sum_net/ppTot
        else: 
            return_per = 0
        context = {
            'holdings':holdings,
            'return_doll':return_doll,
            'return_per': return_per
        }
        return render(request, 'portfolioapp/portfolio.html', context)

    #delete - remove asset from portfolio
    def post(self, request):
        ticker = json.loads(request.body)['ticker']
        holdings = Asset.objects.filter(session = self.request.session.session_key)
        asset = Asset.objects.get(ticker=ticker)
        asset.delete()
        return HttpResponseRedirect(reverse("portfolio-page"))

        

def PortfolioAdd(request,ticker):
    # get modal form to add asset purchase quantity and purchase price
    if request.method == "GET":
        asset_form = AssetForm()
        asset_form.fields['purchase_price'].widget.attrs.update({'placeholder': 0})
        asset_form.fields['purchase_quantity'].widget.attrs.update({'placeholder': 0})
        context= {
            "form" : asset_form,
            "ticker": ticker,
        }
        return render(request, "portfolioapp/add-portfolio.html",context)
    
   #add asset purchase price and quantity to db
    elif request.method == "POST":
        asset_form = AssetForm(request.POST)
    # if form not blank
        if asset_form.is_valid():
            #try:
                # submit to db
                asset = Asset.objects.create(
                    ticker=ticker, 
                    purchase_price = asset_form.cleaned_data['purchase_price'],
                    purchase_quantity = asset_form.cleaned_data['purchase_quantity'],
                    session=request.session.session_key
                )
                asset.save()
                request.session['session_exists'] = False
                request.session['error_exists'] = False
                # direct to portfolio
                return HttpResponseRedirect(reverse("portfolio-page"))
            # delete this - shouldn't be able to add duplicate
            # except IntegrityError:
            #     request.session['error_exists'] = True
            #     return HttpResponseRedirect(reverse("starting-page"))
        # if form is blank, back to same page
        else:
            context  = {
            "form" : asset_form,
            "ticker": asset.ticker,
            }
            return render(request, 'portfolioapp/add-portfolio.html', context)
    

def PortfolioUpdate(request,ticker):
    # get modal form to edit purchase price, quantity
    if request.method == "GET":
        # retrieve users portfolio
        holdings = Asset.objects.filter(session = request.session.session_key)
        # filter to get relevant asset
        asset = get_object_or_404(holdings, ticker=ticker)
        holding_form = HoldingForm()
        pp = asset.purchase_price
        pq = asset.purchase_quantity
        # current stored values as placeholders
        holding_form.fields['purchase_price'].widget.attrs.update({'placeholder': pp})
        holding_form.fields['purchase_quantity'].widget.attrs.update({'placeholder': pq})
        context= {
            "form" : holding_form,
            "ticker": asset.ticker
        }
        return render(request, "portfolioapp/update-portfolio.html",context)

    #post updated asset purchase price and quantity to db
    elif request.method == "POST":
        # if 'update' in request.POST:
        
        holdings = Asset.objects.filter(session = request.session.session_key)
        asset = get_object_or_404(holdings, ticker=ticker)
        holding_form = HoldingForm(request.POST)
        # form isn't blank
        if holding_form.is_valid():
            # saves valid form reponse to databse
            # redirects to portfolio template
            asset.purchase_price = holding_form.cleaned_data['purchase_price']
            asset.purchase_quantity = holding_form.cleaned_data['purchase_quantity']
            asset.save()
            return HttpResponseRedirect(reverse("portfolio-page"))
        # form is blank
        else:
            context  = {
            "form" : holding_form,
            "ticker": asset.ticker,
            "pp": pp,
            "pq": pq
            }
            return render(request, 'portfolioapp/update-portfolio.html', context)
       
        # else:
        #     return HttpResponseRedirect(reverse("portfolio-page"))

    
