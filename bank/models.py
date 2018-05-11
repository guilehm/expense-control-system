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
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='bank')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    agency = models.CharField(max_length=8, blank=True, null=True)
    account_number = models.CharField(max_length=15, blank=True, null=True)
    when_opened = models.DateField()

    def __str__(self):
        return self.bank.name

    @property
    def balance(self):
        return self.total_credits - self.total_debits

    @property
    def total_debits(self):
        return self.debits.all().aggregate(Sum('total'))['total__sum'] or 0.00


    @property
    def total_credits(self):
        return self.credits.all().aggregate(Sum('total'))['total__sum'] or 0.00


class Debit(models.Model):
    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='debits')
    total = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    when = models.DateField()

    def __str__(self):
        return 'Debit_' + str(self.id) + '_in_' + str(self.when)

class Credit(models.Model):
    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='credits')
    total = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    when = models.DateField()

    def __str__(self):
        return 'Credit_' + str(self.id) + '_in_' + str(self.when)


