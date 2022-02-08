from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, DetailView
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import tickerForm

import yfinance as yf
# Create your views here.




# def starting_Page(request):
#     if request.method == "POST":
#         resp = "post"
#         context = {
#             'method': "POST",
#             "tickerform":tickerForm()
#         }
#     else:
#         resp = "get"
#         asset = yf.Ticker('MSFT')
#         context = {
#             # "tickerform":tickerForm(),
#             "asset": asset,
#             "news":asset.news,
#             'ticker': asset.ticker,
#             'method': "GET"
#         }
#     return render (request, 'portfolioapp/index.html', context)


class StartingPageView(View):
    def get(self, request):
        asset = yf.Ticker('MSFT')
        context = {
            "tickerform":tickerForm(),
            "asset": asset,
            "news":asset.news,
            'ticker': asset.ticker,
            'method': "GET"
        }

        return render(request, 'portfolioapp/index.html', context)

    def post(self, request):
        tickerform = tickerForm(request.POST)
        # ticker= tickerform.ticker

        # asset = yf.Ticker(tickerform)

        # asset = yf.Ticker('MSFT')
        
        # if asset exists then:
        context = {
            # "ticker_exists" : True, 
            #        
            'tickerform': tickerForm(),
            'method': "POST"
            # 'response': tickerForm(request.POST),
        }

        #else asset doesn't exist
        #dialog box: enter valid ticker number like msft

        return render(request, 'portfolioapp/index.html', context)


def portfolio(request):
    pass