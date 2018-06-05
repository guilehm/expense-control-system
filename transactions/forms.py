from django import forms

from bank.models import BankAccount
from transactions.models import Expense, Revenue


class ExpenseForm(forms.ModelForm):
    recurrence = forms.IntegerField()

    class Meta:
        model = Expense
        exclude = ('user',)

    def __init__(self, owner, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['account'].queryset = BankAccount.objects.filter(owner=owner)

    def save(self, user, commit=True):
        expense = super().save(commit=False)
        expense.user = user
        expense.account = self.cleaned_data['account']
        expense.title = self.cleaned_data['title']
        expense.description = self.cleaned_data['description']
        expense.total = self.cleaned_data['total']
        expense.competition_date = self.cleaned_data['competition_date']
        expense.due_date = self.cleaned_data['due_date']
        expense.paid_out = self.cleaned_data['paid_out']
        expense.note = self.cleaned_data['note']
        expense.category = self.cleaned_data['category']
        tags = self.cleaned_data['tags']
        expense.save()
        for tag in tags:
            expense.tags.add(tag)
        expense.recurrence = self.cleaned_data['recurrence']

        return expense


class ExpenseEditForm(forms.ModelForm):
    class Meta:
        model = Expense
        exclude = ('user',)

    def __init__(self, owner, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['account'].queryset = BankAccount.objects.filter(owner=owner)


class MultipleExpenseEditForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = (
            'title',
            'account',
            'total',
            'category',
            'due_date',
        )


class ExpenseMultipleEditForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = '__all__'


class RevenueForm(forms.ModelForm):
    class Meta:
        model = Revenue
        exclude = ('user',)

    def __init__(self, owner, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['account'].queryset = BankAccount.objects.filter(owner=owner)


class RevenueEditForm(forms.ModelForm):
    class Meta:
        model = Expense
        exclude = ('user',)

    def __init__(self, owner, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['account'].queryset = BankAccount.objects.filter(owner=owner)
