from django.contrib import admin
from bank.models import BankAccount, Cashing, Deposit

# Register your models here.
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'bank_number', 'owner', 'agency', 'account_number']
    list_filter = ['name', 'bank_number', 'owner',]


class CashingAdmin(admin.ModelAdmin):
    list_display = ['account', 'total', 'user', 'when']
    list_filter = ['account', 'total', 'user', 'when']


class DepositAdmin(admin.ModelAdmin):
    list_display = ['account', 'total', 'user', 'when']
    list_filter = ['account', 'total', 'user', 'when']

admin.site.register(BankAccount, BankAccountAdmin)
admin.site.register(Cashing, CashingAdmin)
admin.site.register(Deposit, DepositAdmin)
