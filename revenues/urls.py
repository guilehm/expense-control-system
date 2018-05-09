from django.urls import path
from . import views


app_name = 'revenues'

urlpatterns = [
    path('', views.index, name='revenues-list'),
]
