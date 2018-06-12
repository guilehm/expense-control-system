from rest_framework.serializers import ModelSerializer
from bank.models import Bank, BankAccount


class BankSerializer(ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'


class BankAccountSerializer(ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'
