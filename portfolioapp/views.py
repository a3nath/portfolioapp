from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, DetailView
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import tickerForm

import yfinance as yf
# Create your views here.

class Starting_page(View):
    
    def get(self, request):

        context = {

            "ticker_form":tickerForm()
            "news": "news"
        }
    return render(request, 'portfolio/app.index.html', context)

    def post(self, request):
        ticker_form = tickerForm(request.POST)
        # asset = yf.Ticker(ticker_form.ticker)
        
        # if asset exists then:

        #     context = {
        #         'ticker_form': tickerForm()
        #         'ticker':"Retrieve Ticker"
        #     }

        #else asset doesn't exist
        #dialog box: enter valid ticker number like msft


    
    msft = yf.Ticker("MSFT")

    return render(request, 'portfolioapp/index.html', context)


    def post(self,request):



def portfolio(request):
    pass