"""controller URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from rest_framework.permissions import AllowAny

from API import views as api_views

router = routers.DefaultRouter()

router.register(r'banks', api_views.BankViewSet)
router.register(r'bank-accounts', api_views.BankAccountViewSet)
router.register(r'categories', api_views.CategoryViewSet)
router.register(r'tags', api_views.TagViewSet)


schema_view = get_schema_view(
   openapi.Info(
      title="ECS",
      default_version='v1',
      description="Expense Control System",
      contact=openapi.Contact(email="guile.hm@hotmail.com"),
   ),
   public=True,
   permission_classes=(AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),
    path('bank/', include('bank.urls', namespace='bank')),
    path('docs/', include_docs_urls(title='ECS')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/', include((router.urls, 'api'), namespace='api')),
    path('accounts/', include('allauth.urls')),
]
