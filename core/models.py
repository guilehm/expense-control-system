import os

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum

from core.validators import csv_file_validator


class CategoryQuerySet(models.QuerySet):
    def total_expenses(self):
        return self.aggregate(Sum('expenses__total'))['expenses__total__sum']

    def total_revenues(self):
        return self.aggregate(Sum('revenues__total'))['revenues__total__sum']


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True, db_index=True)
    date_changed = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        verbose_name_plural = 'Categories'
        unique_together = ('title', 'owner')

    def __str__(self):
        return self.title

    objects = CategoryQuerySet.as_manager()


class Tag(models.Model):
    title = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True, db_index=True)
    date_changed = models.DateTimeField(auto_now=True, db_index=True)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('title', 'owner')


class CSV(models.Model):
    owner = models.ForeignKey(User, related_name='csvs', on_delete=models.CASCADE)
    file = models.FileField(upload_to='core/csv', validators=[csv_file_validator])
    original_file_name = models.CharField(max_length=500, blank=True, null=True)

    date_added = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return os.path.basename(self.file.name)
