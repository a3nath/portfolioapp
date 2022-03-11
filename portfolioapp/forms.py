from django import forms
from django.forms import NumberInput

from .models import Asset

class TickerForm(forms.Form):
    ticker = forms.CharField(max_length=50,required=True, error_messages={'required': 'Please give us a ticker'}, widget=forms.TextInput(attrs={'placeholder': 'MSFT'}))

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        exclude = "__all__"

class HoldingForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['purchase_price', 'purchase_quantity']
        widgets = {
            'purchase_price': NumberInput(attrs={'placeholder': 0}),
            'purchase_quantity': NumberInput(attrs={'placeholder': 0})
        }