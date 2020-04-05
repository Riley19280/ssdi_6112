from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.test import Client
from accounts.models import User
import html


class UserLoginTestCase(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_hello_world(self):
        self.assertTrue(1 == 1, "Test cases are working.")

    def test_valid_login(self):
        response = self.c.post('/login/', {'username': 'testuser', 'password': '12345'})
        self.assertEquals(response.status_code, 302)
        self.assertEqual(response.url, '/dashboard')

    def test_invalid_login(self):
        invalid_response = self.c.post('/login/', {'username': 'testuser', 'password': '123456'})
        self.assertEquals(invalid_response.status_code, 200)
        self.assertContains(invalid_response, 'Please enter a correct username and password.')

    def tearDown(self):
        pass


class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.c = Client()
        self.reg_data = {
            'username': 'testuser123',
            'password1': 'asdf123!!!',
            'password2': 'asdf123!!!',
            'email': 'testuser123@example.com'
        }

    def test_valid_registration(self):
        response = self.c.post('/register', self.reg_data.copy())
        self.assertEquals(response.status_code, 302)
        self.assertEqual(response.url, '/dashboard')

    def test_password_mismatch(self):
        data = self.reg_data.copy()
        data['password2'] = 'wrong'
        invalid_response = self.c.post('/register', data)
        self.assertEquals(invalid_response.status_code, 200)
        self.assertContains(invalid_response, html.escape('The two password fields'))

    def test_password_not_long(self):
        data = self.reg_data.copy()
        data['password1'] = data['password2'] = '1234'
        invalid_response = self.c.post('/register', data)
        self.assertEquals(invalid_response.status_code, 200)
        self.assertContains(invalid_response, html.escape('This password is too short. It must contain at least 8 characters.'))

    def test_password_not_strong(self):
        data = self.reg_data.copy()
        data['password1'] = data['password2'] = '1234asdf'
        invalid_response = self.c.post('/register', data)
        self.assertEquals(invalid_response.status_code, 200)
        self.assertContains(invalid_response, html.escape('This password is too common.'))

    def test_user_exists(self):
        data = self.reg_data.copy()
        invalid_response = self.c.post('/register', data)
        invalid_response = self.c.post('/register', data)
        self.assertEquals(invalid_response.status_code, 200)
        self.assertContains(invalid_response, html.escape('A user with that username already exists.'))

    def tearDown(self):
        pass
