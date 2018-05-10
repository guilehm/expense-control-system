from django.contrib import admin
from bank.models import BankAccount, Cashing, Deposit

# Register your models here.
admin.site.register(BankAccount)
admin.site.register(Cashing)
admin.site.register(Deposit)
