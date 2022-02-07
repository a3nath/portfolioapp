from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, DetailView
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import tickerForm

import yfinance as yf
# Create your views here.

class StartingPageView(View):
    
    def get(self, request):
        asset = yf.Ticker('MSFT')
        print(asset)
        context = {
            # "ticker_exists" : False
            "tickerform":tickerForm(),
            "asset": asset,
            "news":asset.news
        }

        return render(request, 'portfolioapp/index.html', context)

    def post(self, request):
        # tickerform = tickerForm(request.POST)
        # asset = yf.Ticker(tickerform.ticker)
        
        # if asset exists then:
        context = {
            # "ticker_exists" : True,        
            'tickerform': tickerForm(),
            'ticker':"Retrieve Ticker",
            'response': tickerForm(request.POST)
        }

        #else asset doesn't exist
        #dialog box: enter valid ticker number like msft

        return render(request, 'portfolioapp/index.html', context)


def portfolio(request):
    pass