from django.test import TestCase, Client
from django.contrib.auth.models import User

from model_mommy import mommy


class PagesTestView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = mommy.prepare(User, username='guilherme')
        self.user.set_password('password')
        self.user.save()
        self.client.login(username='guilherme', password='pas   sword')

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/base.html')
        self.assertTemplateUsed(response, 'core/index.html')
