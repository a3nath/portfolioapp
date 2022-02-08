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
        # asset_id = request.session['search_ticker']
        # try:
        #     asset = yf.Ticker("MSFT")
        # except:
        #     print("Try a new ticker hommie!")
        
        context = {
            # "is_searched": ,
            # 'asset_id':request.session['search_ticker']
            "tickerform":tickerForm(),
            # "asset": asset,
            # "news":asset.news,
            'method': "GET"
        }

        return render(request, 'portfolioapp/index.html', context)

    def post(self, request):
        tickerform = tickerForm(request.POST)
        # request.session['search_ticker'] = tickerform.ticker
        # ticker= tickerform.ticker

        # asset = yf.Ticker(tickerform)

        # asset = yf.Ticker('MSFT')
        
        # if asset exists then:
        context = {
            # "ticker_exists" : True, 
            #        
            'tickerform': tickerForm,
            'method': "POST"
            # 'response': tickerForm(request.POST),
        }

        #else asset doesn't exist
        #dialog box: enter valid ticker number like msft

        return HttpResponseRedirect(reverse('starting-page'))


def portfolio(request):
    pass