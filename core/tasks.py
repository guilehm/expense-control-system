# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.contrib.auth.models import User

from core.models import Tag


@shared_task
def add(x, y):
    return x + y


@shared_task
def create_tag():
    Tag.objects.create(owner=User.objects.first(), title='Celery', slug='celery-tag')
