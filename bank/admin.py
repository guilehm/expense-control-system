from django.contrib import admin
from bank.models import Bank, BankAccount

# Register your models here.
class BankAdmin(admin.ModelAdmin):
    list_display = ['name', 'number']

class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['bank','owner', 'agency', 'account_number']
    list_filter = ['owner',]


class DebitAdmin(admin.ModelAdmin):
    list_display = ['account', 'total', 'user', 'when']
    list_filter = ['account', 'total', 'user', 'when']


class CreditAdmin(admin.ModelAdmin):
    list_display = ['account', 'total', 'user', 'when']
    list_filter = ['account', 'total', 'user', 'when']

admin.site.register(Bank, BankAdmin)
admin.site.register(BankAccount, BankAccountAdmin)
