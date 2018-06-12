from django.urls import path

from . import views

app_name = 'API'

urlpatterns = [
        path('bank-list/', views.BankList.as_view(), name='bank-list')
]