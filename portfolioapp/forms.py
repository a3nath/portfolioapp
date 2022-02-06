from django import forms

class tickerForm(forms.Form):
    ticker = forms.CharField(label='Ticker name', max_length=50)