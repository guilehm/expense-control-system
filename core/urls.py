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
    path('expenses/', views.expense_list, name='expenses'),
    path('revenues/', views.revenue_list, name='revenues'),
    path('expenses/include/', views.expense_include, name='expenses-include'),
    path('revenues/include/', views.revenue_include, name='revenues-include'),
    path('revenues/edit/<int:revenue_id>/', views.revenue_edit, name='revenues-edit'),
    path('expenses/edit/<int:expense_id>/', views.expense_edit, name='expenses-edit'),
    path('bank-accounts/create/', views.bank_accounts_create, name='bank-accounts-create'),
    path('categories/include/', views.category_include, name='categories-include'),
    path('category/<str:category_slug>/', views.category_detail, name='categories-detail'),
    path('api/', views.api_list, name='api-list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
