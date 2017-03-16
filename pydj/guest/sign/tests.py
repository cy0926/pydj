from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.test.utils import setup_test_environment

setup_test_environment()


# Create your tests here.
class IndexPageTest(TestCase):
    def test_index_page_reders_index_template(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response, 'index.html')


class LoginActionTest(TestCase):
    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        self.c = Client()

    def test_login_action_username_password_null(self):
        test_data = {'username': '', 'password': ''}
        response = self.c.post('login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or password error", response.content)
