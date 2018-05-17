from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('expenses/include', views.expenses_include, name='expenses-include'),
    path('bank-accounts/create', views.bank_accounts_create, name='bank-accounts-create'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
