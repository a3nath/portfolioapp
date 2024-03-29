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
import locale


import yfinance as yf


class StartingPageView(View):
    def get(self, request):
        ##searched already
            if request.session.get('session_exists'): 
                ticker_input = request.session.get('ticker_input')
                ticker_asset = yf.Ticker(ticker_input)
            #invalid ticker
                if not ticker_asset.isin.isalnum():
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
        portfolio_val = 0
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
                holding.tot_val = round(cp*pq)
                holding.net_val = round((cp-pp)*pq)
            else: 
                pp = 0
                pq = 0
                cp = 0
            return_doll += round((cp - pp)*pq)
            sum_net += (cp - pp)*pq
            ppTot += pp*pq
            portfolio_val += holding.tot_val
        if ppTot > 0:
            return_per = round(sum_net/ppTot * 100)
        #not purchased anything so far
        else: 
            return_per = 0

        locale.setlocale(locale.LC_ALL, 'en_US')

        context = {
            'holdings':holdings,
            'return_doll':locale.format("%d", return_doll, grouping=True),
            'return_per': return_per,
            'portfolio_val':  locale.format("%d", portfolio_val, grouping=True)
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
        if 'addticker' in request.POST:
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
            # form is blank, back to same page
            else:
                context  = {
                "form" : asset_form,
                "ticker": asset.ticker,
                }
                return render(request, 'portfolioapp/add-portfolio.html', context)
        else:
            return HttpResponseRedirect(reverse("starting-page"))
            
    

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
        if 'updateticker' in request.POST:
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
        else:
            return HttpResponseRedirect(reverse("portfolio-page"))

    
