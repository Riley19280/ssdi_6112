from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.test import Client
from accounts.models import User


class UserLoginTestCase(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_hello_world(self):
        self.assertTrue(1 == 1, "Test cases are working.")

    def test_valid_login(self):
        response = self.c.post('/login/', {'username': 'testuser', 'password': '12345'})
        self.assertEquals(response.status_code, 302)

    def test_invalid_login(self):
        invalid_response = self.c.post('/login/', {'username': 'testuser', 'password': '123456'})
        self.assertEquals(invalid_response.status_code, 200)
        self.assertContains(invalid_response, 'Please enter a correct username and password.')

    def tearDown(self):
        pass
