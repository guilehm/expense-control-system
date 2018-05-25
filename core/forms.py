from django import forms

from bank.models import BankAccount
from transactions.models import Revenue

class BankAccountCreateForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        exclude = [
            'owner',
        ]


class RevenueEditForm(forms.ModelForm):
    class Meta:
        model = Revenue
        fields = '__all__'
