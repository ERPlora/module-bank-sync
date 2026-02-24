from django import forms
from django.utils.translation import gettext_lazy as _

from .models import BankAccount, BankTransaction

class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['name', 'bank_name', 'account_number', 'iban', 'currency', 'balance', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'bank_name': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'account_number': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'iban': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'currency': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'balance': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'toggle'}),
        }

class BankTransactionForm(forms.ModelForm):
    class Meta:
        model = BankTransaction
        fields = ['account', 'date', 'description', 'amount', 'balance_after', 'is_reconciled', 'reference']
        widgets = {
            'account': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'date': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'date'}),
            'description': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'amount': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
            'balance_after': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
            'is_reconciled': forms.CheckboxInput(attrs={'class': 'toggle'}),
            'reference': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
        }

