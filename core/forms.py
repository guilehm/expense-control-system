from django import forms
from bank.models import BankAccount

class BankAccountCreateForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        exclude = [
            'owner',
        ]
