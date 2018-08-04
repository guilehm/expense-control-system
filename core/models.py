from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


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
