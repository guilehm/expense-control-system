from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User


class ExpenseQuerySet(models.QuerySet):
    def total(self):
        return self.aggregate(Sum('total'))['total__sum'] or 0


class RevenueQuerySet(models.QuerySet):
    def total(self):
        return self.aggregate(Sum('total'))['total__sum'] or 0


# Create your models here.
class Revenue(models.Model):
    account = models.ForeignKey('bank.BankAccount', on_delete=models.CASCADE, related_name='revenues')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    total = models.DecimalField(max_digits=9, decimal_places=2)
    competition_date = models.DateField(db_index=True, blank=True, null=True)
    due_date = models.DateField(db_index=True)
    received_out = models.BooleanField(default=False)
    note = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        'core.Category',
        related_name='revenues',
        on_delete=models.CASCADE,
    )
    tags = models.ManyToManyField(
        'core.Tag',
        related_name='revenues',
        blank=True,
    )

    objects = RevenueQuerySet.as_manager()

    date_added = models.DateTimeField(auto_now_add=True, db_index=True)
    date_changed = models.DateTimeField(auto_now=True, db_index=True)

    def __str__(self):
        return self.title


class Expense(models.Model):
    account = models.ForeignKey('bank.BankAccount', on_delete=models.CASCADE, related_name='expenses')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    total = models.DecimalField(max_digits=9, decimal_places=2)
    competition_date = models.DateField(db_index=True, blank=True, null=True)
    due_date = models.DateField(db_index=True)
    paid_out = models.BooleanField(default=False)
    note = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        'core.Category',
        related_name='expenses',
        on_delete=models.CASCADE,
    )
    tags = models.ManyToManyField(
        'core.Tag',
        related_name='expenses',
        blank=True,
    )

    objects = ExpenseQuerySet.as_manager()

    date_added = models.DateTimeField(auto_now_add=True, db_index=True)
    date_changed = models.DateTimeField(auto_now=True, db_index=True)

    def __str__(self):
        return self.title

    # FIXME: just for testing, improve if works
    def update_total(self, value):
        if value >= 0:
            self.total = value
