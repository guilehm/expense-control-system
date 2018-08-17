from rest_framework.response import Response
from rest_framework.views import APIView

from API.serializers import BankAccountSerializer, BankSerializer, CategorySerializer, TagSerializer
from bank.models import Bank, BankAccount
from core.models import Category, Tag


# Create your views here.
class BankList(APIView):
    def get(self, request):
        banks = Bank.objects.all()
        serializer = BankSerializer(banks, context={'request': request}, many=True)
        return Response(serializer.data)


class BankAccountList(APIView):
    def get(self, request):
        bank_accounts = BankAccount.objects.filter(owner=request.user)
        serializer = BankAccountSerializer(bank_accounts, context={'request': request}, many=True)
        return Response(serializer.data)


class CategoryList(APIView):
    def get(self, request):
        categories = Category.objects.filter(owner=request.user)
        serializer = CategorySerializer(categories, context={'request': request}, many=True)
        return Response(serializer.data)


class TagList(APIView):
    def get(self, request):
        tags = Tag.objects.filter(owner=request.user)
        serializer = TagSerializer(tags, context={'request': request}, many=True)
        return Response(serializer.data)
