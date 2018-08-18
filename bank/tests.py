import pytest
from django.urls import reverse
from rest_framework import status

from bank.models import Bank


@pytest.mark.django_db
class TestBankViews:

    @pytest.fixture
    def banks_endpoint(self):
        return reverse('API:bank-list')

    @pytest.fixture
    def banks_payload(self, bank):
        return [
            {
                "id": bank.id,
                "name": bank.name,
                "number": bank.number,
                "img": bank.img
            },
        ]

    @pytest.fixture
    def bank_accounts_payload(self, bank_account, bank_account_two):
        return [
            {
                "id": bank_account.id,
                "agency": bank_account.agency,
                "account_number": bank_account.account_number,
                "when_opened": bank_account.when_opened.isoformat(),
                "bank": bank_account.bank.id,
                "owner": bank_account.owner.id
            },
            {
                "id": bank_account_two.id,
                "agency": bank_account_two.agency,
                "account_number": bank_account_two.account_number,
                "when_opened": bank_account_two.when_opened.isoformat(),
                "bank": bank_account_two.bank.id,
                "owner": bank_account_two.owner.id
            },
        ]

    def test_should_return_correct_bank_payload(
            self,
            public_client,
            bank,
            banks_payload,
            banks_endpoint,
    ):
        response = public_client.get(banks_endpoint)
        json_response = response.json()
        assert Bank.objects.count() == 1
        assert Bank.objects.first() == bank
        assert response.status_code == status.HTTP_200_OK
        assert json_response == banks_payload
