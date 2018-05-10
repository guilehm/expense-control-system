from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True, db_index=True)
    date_changed = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True, db_index=True)
    date_changed = models.DateTimeField(auto_now=True, db_index=True)

    def __str__(self):
        return self.title


class BankAccount(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    agency = models.CharField(max_length=6, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    when_opened = models.DateField()


class Deposit(models.Model):
    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    total = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    when = models.DateTimeField()


class Cashing(models.Model):
    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    total = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    when = models.DateTimeField()
