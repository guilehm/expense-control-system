from model_mommy import mommy
import pytest
from transactions.models import Revenue, Expense


@pytest.mark.django_db
class TestExpenseModels:

    def test_should_create_expenses(self, expenses):
        assert Expense.objects.count() == 50

    def test_should_link_expenses_to_right_user(self, expenses, user):
        for expense in expenses:
            assert expense.user == user


@pytest.mark.django_db
class TestRevenueModels:

    def test_should_create_revenues(self, revenues):
        assert Revenue.objects.count() == 50

    def test_should_link_revenues_to_right_user(self, revenues, user):
        for revenue in revenues:
            assert revenue.user == user
