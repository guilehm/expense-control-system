from django.urls import path

from . import views

app_name = 'API'

urlpatterns = [
    path('bank-list/', views.BankList.as_view(), name='bank-list'),
    path('bank-account-list/', views.BankAccountList.as_view(), name='bank-account-list'),
    path('category-list/', views.CategoryList.as_view(), name='category-list'),
]
