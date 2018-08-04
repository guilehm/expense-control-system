from rest_framework.serializers import ModelSerializer

from bank.models import Bank, BankAccount
from core.models import Category, Tag


class BankSerializer(ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'


class BankAccountSerializer(ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
