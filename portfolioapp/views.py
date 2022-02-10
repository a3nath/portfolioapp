from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, DetailView
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import tickerForm

import yfinance as yf
# Create your views here.


# if request get
# access asset
#session['ticker'] = ticker
#within get I can check if it exists or not
##if it does then asset = something otherwise something for context
##Do I need context for post?
##save session info at post and ask from there at get


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

        if request.session.get('ticker_exists'): 
            ticker = request.session.get('ticker')
            asset = yf.Ticker('MSFT')
            news = asset.news
        else:
            ticker = "DNE"
            asset = ''
            news = ''
        context = {
            # "is_searched": ,
            # 'asset_id':request.session['search_ticker']
            "tickerform":tickerForm(),
            # "asset": asset,
            # "news":asset.news,
            'method': "GET",
            'ticker': ticker,
            'news':news
        }

        return render(request, 'portfolioapp/index.html', context)

    def post(self, request):
        ticker_form = tickerForm(request.POST)
        if ticker_form.is_valid():
            ticker = ticker_form.cleaned_data['ticker']
            request.session['ticker'] = ticker
            request.session['ticker_exists'] = True
            
            
        # request.session['search_ticker'] = tickerform.ticker
        # ticker= tickerform.ticker

        # asset = yf.Ticker(tickerform)

        # asset = yf.Ticker('MSFT')
        
        # if asset exists then:
    #  context = {
    #         # "ticker_exists" : True, 
    #         #        
    #         'method': "POST",
    #         'ticker':ticker
    #         # 'response': tickerForm(request.POST),
    #     }

        #else asset doesn't exist
        #dialog box: enter valid ticker number like msft

        return HttpResponseRedirect(reverse('starting-page'))


def portfolio(request):
    pass