import pytest
from django.contrib.auth.models import User
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
def bank_account(bank, user):
    return mommy.make(
        'bank.BankAccount',
        owner=user,
        bank=bank,
        agency='1440',
        account_number='14404-4'
    )


@pytest.fixture
def bank_account_two(bank, user):
    return mommy.make(
        'bank.BankAccount',
        owner=user,
        bank=bank,
        agency='9440',
        account_number='94404-4'
    )


@pytest.fixture
def user():
    user = mommy.prepare(User)
    user.set_password('password')
    user.save()
    return user
