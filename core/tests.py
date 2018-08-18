import pytest
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from model_mommy import mommy
from rest_framework import status

from core.models import Category, Tag


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
        assert response.status_code == status.HTTP_200_OK
        assert json_response == category_payload


@pytest.mark.django_db
class TestCategoryModels:

    def test_should_create_category(self, category):
        assert Category.objects.count() == 1
        assert Category.objects.first() == category

    def test_should_link_category_to_right_user(self, user, user_two, category):
        assert Category.objects.first() == category
        assert Category.objects.first().owner == user
        assert Category.objects.first().owner != user_two


@pytest.mark.django_db
class TestTagViews:

    @pytest.fixture
    def tag_endpoint(self):
        return reverse('API:tag-list')

    @pytest.fixture
    def tag_payload(self, tag, user):
        return [
            {
                "id": tag.id,
                "title": tag.title,
                "slug": tag.slug,
                "description": tag.description,
                "date_added": tag.date_added.isoformat().replace('+00:00', 'Z'),
                "date_changed": tag.date_changed.isoformat().replace('+00:00', 'Z'),
                "owner": user.id,
            },
        ]

    def test_should_return_correct_tag_payload(
            self,
            user,
            tag,
            public_client,
            tag_payload,
            tag_endpoint,
    ):
        public_client.force_login(user)
        response = public_client.get(tag_endpoint)
        json_response = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert json_response == tag_payload


@pytest.mark.django_db
class TestTagModels:

    def test_should_create_tag(self, tag):
        assert Tag.objects.count() == 1
        assert Tag.objects.first() == tag

    def test_should_link_tag_to_right_user(self, user, user_two, tag):
        assert Tag.objects.first() == tag
        assert Tag.objects.first().owner == user
        assert Tag.objects.first().owner != user_two
