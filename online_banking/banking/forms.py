# banking/forms.py
from django import forms
from decimal import Decimal
from .models import Account

class DepositForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal('0.01'), # Must deposit at least 1 paisa
        widget=forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'Enter amount'})
    )

class WithdrawForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal('0.01'),
        widget=forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'Enter amount'})
    )

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account', None) # Pass the account to the form
        super().__init__(*args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if self.account and amount:
            if self.account.balance < amount:
                raise forms.ValidationError("Insufficient funds.")
        elif not self.account:
             raise forms.ValidationError("Account information missing.") # Should not happen normally
        return amount