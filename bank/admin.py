from django.contrib import admin
from bank.models import BankAccount, Debit, Credit

# Register your models here.
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'bank_number', 'owner', 'agency', 'account_number']
    list_filter = ['name', 'bank_number', 'owner',]


class DebitAdmin(admin.ModelAdmin):
    list_display = ['account', 'total', 'user', 'when']
    list_filter = ['account', 'total', 'user', 'when']


class CreditAdmin(admin.ModelAdmin):
    list_display = ['account', 'total', 'user', 'when']
    list_filter = ['account', 'total', 'user', 'when']

admin.site.register(BankAccount, BankAccountAdmin)
admin.site.register(Debit, DebitAdmin)
admin.site.register(Credit, CreditAdmin)
