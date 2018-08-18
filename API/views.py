from rest_framework import viewsets

from django_filters import FilterSet

from rest_framework.permissions import AllowAny
from API.serializers import BankAccountSerializer, BankSerializer, CategorySerializer, TagSerializer
from bank.models import Bank, BankAccount
from core.models import Category, Tag


class TagFilterSet(FilterSet):
    class Meta:
        model = Tag
        fields = [
            'title',
            'slug',
            'description',
            'date_added',
            'date_changed',
            'owner',
        ]


# Create your views here.
class BankViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    permission_classes = (AllowAny,)


class BankAccountViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return BankAccount.objects.filter(owner=self.request.user)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Tag.objects.filter(owner=self.request.user)
