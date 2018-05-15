from django import forms

from transactions.models import Expense, Revenue

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        exclude = ('user',)


class RevenueForm(forms.ModelForm):
    class Meta:
        model = Revenue
        fields = '__all__'
