from django import forms

from .models import Asset

class TickerForm(forms.Form):
    ticker = forms.CharField(label='Ticker name', max_length=50)

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        exclude = "__all__"

class HoldingForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['purchase_price', 'purchase_quantity']
