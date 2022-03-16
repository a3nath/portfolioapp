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
        if request.session.get('error_exists'):
            context ={
                "errExists": True,
                'message':  request.session.get('message'),
                "ticker_form":TickerForm()
            }
            request.session['error_exists'] = False
            request.session['message'] = ''
            # render(request, 'portfolioapp/index.html', context)  
        else:
            if request.session.get('session_exists'): 
                ticker_input = request.session.get('ticker_input')
                ticker_asset = yf.Ticker(ticker_input)
                info = ticker_asset.info
                if info["regularMarketPrice"] == None:
                    #invalid ticker then set valid ticker identifier False
                    ticker_valid = False
                    # error exists that ticker doesnt exist
                    request.session['error_exists'] = True
                    request.session['message'] = 'Asset doesnt Exist'
                    context = {
                    "ticker_form":TickerForm(),
                    'ticker_valid': ticker_valid,
                    "message": request.session.get('message')
                    }
                else:
                    #valid ticker then set valid identifier True 
                    ticker_valid = True 
                    # switch session exists to False otherwse it will show current data at refresh
                    request.session['session_exists'] = False
                    request.session['ticker_name'] = ticker_input 
                    # no error
                    request.session['error_exists'] = False
                    
                    context = {
                    "ticker_form":TickerForm(),
                    "ticker_valid": ticker_valid,
                    "news": ticker_asset.news,
                    "message": request.session.get('message')
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
        if 'searchticker' in request.POST:
            #if search button is clicked
            ticker_form = TickerForm(request.POST)
            if ticker_form.is_valid():
            #form isnt blank
                ticker_input = ticker_form.cleaned_data['ticker'].lower()
                request.session['ticker_input'] = ticker_input
                request.session['session_exists'] = True
            else:
            #form is blank
                request.session['message'] = "form is blank"
                request.session['session_exists'] = False
        elif 'addasset' in request.POST:
            try:
            # add response to user portfolio
                request.session['error_exists'] = False
                request.session['message'] = "Asset added successfully"
                asset = Asset.objects.create(ticker=request.session.get('ticker_name'), session=request.session.session_key)
                ##save user input
                asset.save()
                ##show asset info even after user adds
                request.session['session_exists'] = True
                
                ##NEED POP UP THAT SAYS ASSET ADDED
            except IntegrityError:
            # asset already exists in portfolio
            # stops adding duplicate
                request.session['error_exists'] = True
                request.session['message'] = "Assets exisits in your portfolio already. Please try another asset"
        return HttpResponseRedirect(reverse('starting-page'))
                      
class PortfolioPageView(View):
    def get(self, request):
        holdings = Asset.objects.filter(session = self.request.session.session_key)
        return_doll = 0
        sum_net = 0 
        ppTot = 0
        for holding in holdings:
              # for each holding
            # get purchase_price, purchase_q
            # get closing price

            ticker_asset = yf.Ticker(holding.ticker)
            holding.closing_price = round(ticker_asset.history(period="1d").iloc[0]["Close"])
            if holding.purchase_price:
                pp = holding.purchase_price
                pq = holding.purchase_quantity
                cp = holding.closing_price    
                holding.total_return = round(pp*pq)
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

    def post(self, request):
        ticker = json.loads(request.body)['ticker']
        holdings = Asset.objects.filter(session = self.request.session.session_key)
        asset = Asset.objects.get(ticker=ticker)
        asset.delete()
        # print('Hello Im ' % self.request.POST.get('_method'))
        return HttpResponseRedirect(reverse("portfolio-page"))

        


# def portfolioPage(request):
#     if request.method == 'GET':
#         holdings = Asset.objects.filter(session = request.session.session_key)
#         return_doll = 0
#         sum_net = 0 
#         ppTot = 0
#         for holding in holdings:
#               # for each holding
#             # get purchase_price, purchase_q
#             # get closing price
#             if holding.purchase_price:
#                 pp = holding.purchase_price
#                 pq = holding.purchase_quantity
#                 ticker_asset = yf.Ticker(holding.ticker)
#                 cp = ticker_asset.history(period="1d").iloc[0]["Close"]
#             else: 
#                 pp = 0
#                 pq = 0
#                 cp = 0
#             return_doll += (cp - pp)*pq
#             sum_net += (cp - pp)
#             ppTot += pp
#         if ppTot > 0:
#             return_per = sum_net/ppTot
#         else: 
#             return_per = 0
#         context = {
#             'holdings':holdings,
#             'return_doll':return_doll,
#             'return_per': return_per
#         }
#         return render(request, 'portfolioapp/portfolio.html', context)
#         # delete a ticker
#     elif request.method == "DELETE":
#         holdings = Asset.objects.filter(session = request.session.session_key)
#         asset = Asset.objects.get(ticker=ticker)
#         print('method delete')
#         asset.delete()
#         return HttpResponse(status=204)

    

def PortfolioUpdate(request,ticker):
    if request.method == "GET":
        # show asset specific info
        # asset ticker
        # asset purchase quantity and purchase price
        holdings = Asset.objects.filter(session = request.session.session_key)
        asset = get_object_or_404(holdings, ticker=ticker)
        holding_form = HoldingForm()
        pp = asset.purchase_price
        pq = asset.purchase_quantity
        holding_form.fields['purchase_price'].widget.attrs.update({'placeholder': pp})
        holding_form.fields['purchase_quantity'].widget.attrs.update({'placeholder': pq})
        context= {
            "form" : holding_form,
            "ticker": asset.ticker,
            "pp": pp,
            "pq": pq
        }
        return render(request, "portfolioapp/update-portfolio.html",context)
    # ##post
    # ##submit form and update values in db
    elif request.method == "POST":
        if 'update' in request.POST:
            holdings = Asset.objects.filter(session = request.session.session_key)
            asset = get_object_or_404(holdings, ticker=ticker)
            holding_form = HoldingForm(request.POST)
            if holding_form.is_valid():
                # saves valid form reponse to databse
                # redirects to portfolio template
                asset.purchase_price = holding_form.cleaned_data['purchase_price']
                asset.purchase_quantity = holding_form.cleaned_data['purchase_quantity']
                asset.save()
                return HttpResponseRedirect(reverse("portfolio-page"))
            else:
                # if form isn't valid
                context  = {
                "form" : holding_form,
                "ticker": asset.ticker,
                "pp": pp,
                "pq": pq
                }
                return render(request, 'portfolioapp/update-portfolio.html', context)
        else:
            return HttpResponseRedirect(reverse("portfolio-page"))

    
