import pytest
from django.urls import reverse

from rest_framework import status


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

    def test_should_return_correct_payload(
            self,
            public_client,
            bank,
            banks_payload,
            banks_endpoint,
    ):
        response = public_client.get(banks_endpoint)
        json_response = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert json_response == banks_payload
