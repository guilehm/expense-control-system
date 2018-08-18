import pytest
from model_mommy import mommy
from rest_framework.test import APIClient


@pytest.fixture
def public_client():
    client = APIClient()
    return client


@pytest.fixture
def bank():
    return mommy.make('bank.Bank')


@pytest.fixture
def bank_account(bank):
    return mommy.make(
        'bank.BankAccount',
        bank=bank,
        agency='1440',
        account_number='14404-4'
    )
