from django.forms import ModelForm
from .models import Sale, Holding, Account


class SaleForm(ModelForm):
    class Meta:
        model = Sale
        fields = ['type', 'date', 'sale_quantity', 'sale_price']


class HoldingForm(ModelForm):
    class Meta:
        model = Holding
        fields = ['ticker']


class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['cash', 'capital_gains', 'capital_losses']
