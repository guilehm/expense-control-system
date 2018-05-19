from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User


class Bank(models.Model):
    name = models.CharField(max_length=50)
    number = models.CharField(max_length=3)
    img = models.ImageField(upload_to='bank/logos', blank=True, null=True)

    def __str__(self):
        return self.name


class BankAccount(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='accounts')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    agency = models.CharField(max_length=8, blank=True, null=True)
    account_number = models.CharField(max_length=15, blank=True, null=True)
    when_opened = models.DateField()

    def __str__(self):
        return self.bank.name

    @property
    def balance(self):
        return self.total_received_revenues - self.total_paid_expenses

    @property
    def total_expenses(self):
        return self.expenses.all().aggregate(Sum('total'))['total__sum'] or 0

    @property
    def total_paid_expenses(self):
        return self.expenses.filter(paid_out=True).aggregate(Sum('total'))['total__sum'] or 0

    @property
    def total_expenses_to_pay(self):
        return self.total_expenses - self.total_paid_expenses

    @property
    def total_revenues(self):
        return self.revenues.all().aggregate(Sum('total'))['total__sum'] or 0

    @property
    def total_received_revenues(self):
        return self.revenues.filter(received_out=True).aggregate(Sum('total'))['total__sum'] or 0

    @property
    def total_revenues_to_receive(self):
        return self.total_revenues - self.total_received_revenues
