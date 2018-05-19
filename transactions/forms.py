from django import forms

from bank.models import BankAccount
from transactions.models import Expense, Revenue

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        exclude = ('user',)

    def __init__(self, owner, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['account'].queryset = BankAccount.objects.filter(owner=owner)


class ExpenseEditForm(forms.ModelForm):
    class Meta:
        model = Expense
        exclude = ('user',)

    def __init__(self, owner, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['account'].queryset = BankAccount.objects.filter(owner=owner)


class RevenueForm(forms.ModelForm):
    class Meta:
        model = Revenue
        fields = '__all__'
