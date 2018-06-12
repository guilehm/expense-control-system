from rest_framework.views import APIView
from rest_framework.response import Response

from API.serializers import BankSerializer
from bank.models import Bank


# Create your views here.
class BankList(APIView):
    def get(self, request):
        banks = Bank.objects.all()
        serializer = BankSerializer(banks, context={'request': request}, many=True)
        return Response(serializer.data)