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
    user = User.objects.create(username='Guilherme', password='Django')
    user.save()
    return user


@pytest.fixture
def user_two():
    user_two = User.objects.create(username='Gui', password='Django2')
    user_two.save()
    return user_two


@pytest.fixture
def category(user):
    return mommy.make('core.Category', owner=user)


@pytest.fixture
def tag(user):
    return mommy.make('core.Tag', owner=user)


@pytest.fixture
def expenses(user, bank_account):
    return mommy.make(
        'transactions.Expense', user=user, account=bank_account, _quantity=50
    )


@pytest.fixture
def revenues(user, bank_account):
    return mommy.make(
        'transactions.Revenue', user=user, account=bank_account, _quantity=50
    )


@pytest.fixture
def expenses_fixed(user, bank_account):
    return mommy.make(
        'transactions.Expense',
        user=user,
        account=bank_account,
        _quantity=50,
        total=10
    )
