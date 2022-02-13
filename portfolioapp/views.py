from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, DetailView
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import TickerForm, AssetForm
from .models import Asset


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

        if request.session.get('session_exists'): 
            ticker_input = request.session.get('ticker_input')
            ###try except
            ticker_asset = yf.Ticker(ticker_input)
            info = ticker_asset.info
            if info["regularMarketPrice"] == None:
                ticker_valid = False
            else:
                ticker_valid = True   
                request.session['ticker_name'] = ticker_input
                # request.session['closing_price'] = asset.history(period="1d")['Close']
        else:
            ticker_valid = False

        if ticker_valid:
            context = {
                "ticker_form":TickerForm(),
                "ticker_valid": True,
                "news": ticker_asset.news
                # "asset_form": AssetForm()
            }
            request.session['session_exists'] = False
        else:
            context = {
                "ticker_form":TickerForm(),
                'ticker_valid': False,
                'news': '',
            }
            request.session['session_exists'] = False

        return render(request, 'portfolioapp/index.html', context)

            # try:
            #     asset = yf.Ticker(ticker)
            #     info = asset.info
            # except ConnectionError:
            #     raise ConnectionError("CON")
            # except TimeoutError:
            #     raise TimeoutError("TIME")
            # except Exception:
            #     raise ValueError("VALS")
        
        # context = {
        #     # "is_searched": ,
        #     # 'asset_id':request.session['search_ticker']
         
        #     # "asset": asset,
        #     # "news":asset.news,
        #     'method': "GET",
        #     'news':news,
        # }

      

    def post(self, request):
        if 'searchticker' in request.POST:
            ticker_form = TickerForm(request.POST)
            if ticker_form.is_valid():
                ticker_input = ticker_form.cleaned_data['ticker']
                request.session['ticker_input'] = ticker_input
                request.session['session_exists'] = True
            else:
                request.session['session_exists'] = False
            # return HttpResponseRedirect(reverse("starting-page"))
        elif 'addasset' in request.POST:
            # asset_form = AssetForm(request.POST)
            # if asset_form.is_valid():
                asset = Asset.objects.create(ticker=request.session.get('ticker_name'), session=request.session.session_key)
                ##save user input
                # asset = asset_form.save(commit=False)
                ##add session
                asset.save()
            # else:
            #     pass
            # return HttpResponseRedirect(reverse("starting-page"))
        return HttpResponseRedirect(reverse('starting-page'))


        

            
            
        # request.session['search_ticker'] = tickerform.ticker
        # ticker= tickerform.ticker

        # asset = yf.Ticker(tickerform)

        # asset = yf.Ticker('MSFT')
        
        # if asset exists then:
    #  context = {
    #         # "session_exists" : True, 
    #         #        
    #         'method': "POST",
    #         'ticker':ticker
    #         # 'response': tickerForm(request.POST),
    #     }

        #else asset doesn't exist
        #dialog box: enter valid ticker number like msft

    
class PortfolioPageView(ListView):
    template_name = 'portfolioapp/portfolio.html'
    model = Asset
    context_object_name = 'holdings'
   
    def get_queryset(self):
       base_query = super().get_queryset()
       data = base_query.filter(session = self.request.session.session_key)
       return data

