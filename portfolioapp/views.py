from django.shortcuts import render
from django.http import HttpResponse
from .forms import CommentForm
from django.views import View
from django.views.generic import ListView, DetailView
from django.http import HttpResponseRedirect
from django.urls import reverse

import yfinance as yf
# Create your views here.

def index(request):
    msft = yf.Ticker("MSFT")
    context = {
        "msft": msft
    }
    return render(request, 'portfolioapp/index.html', context)