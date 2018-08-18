from django.contrib.auth.models import User
from django.test import Client, TestCase
from model_mommy import mommy
import pytest
from core.models import Category, Tag
from django.urls import reverse
from rest_framework import status


class PagesTestView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = mommy.prepare(User, username='guilherme')
        self.user.set_password('password')
        self.user.save()
        self.client.login(username='guilherme', password='password')

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/base.html')
        self.assertTemplateUsed(response, 'core/index.html')


@pytest.mark.django_db
class TestCategoryViews:

    @pytest.fixture
    def category_endpoint(self):
        return reverse('API:category-list')

    @pytest.fixture
    def category_payload(self, category, user):
        return [
            {
                "id": category.id,
                "title": category.title,
                "slug": category.slug,
                "description": category.description,
                "date_added": category.date_added.isoformat().replace('+00:00', 'Z'),
                "date_changed": category.date_changed.isoformat().replace('+00:00', 'Z'),
                "owner": user.id,
            },
        ]

    def test_should_return_correct_category_payload(
            self,
            user,
            category,
            public_client,
            category_payload,
            category_endpoint,
    ):
        public_client.force_login(user)
        response = public_client.get(category_endpoint)
        json_response = response.json()
        assert Category.objects.count() == 1
        assert response.status_code == status.HTTP_200_OK
        assert json_response == category_payload
