from rest_framework.views import APIView
from rest_framework.response import Response

from API.serializers import BankSerializer, BankAccountSerializer
from bank.models import Bank, BankAccount


# Create your views here.
class BankList(APIView):
    def get(self, request):
        banks = Bank.objects.all()
        serializer = BankSerializer(banks, context={'request': request}, many=True)
        return Response(serializer.data)


# Create your views here.
class BankAccountList(APIView):
    def get(self, request):
        bank_accounts = BankAccount.objects.all()
        serializer = BankAccountSerializer(bank_accounts, context={'request': request}, many=True)
        return Response(serializer.data)