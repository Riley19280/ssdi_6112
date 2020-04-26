from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.conf import settings
import shutil
import os

from accounts.models import User
import html


class FileUploadTestCase(TestCase):

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.c.force_login(self.user)

    def test_dataset_upload(self):
        path = os.path.join(settings.MEDIA_ROOT, 'graphs', str(self.user.id), 'test_dataset')
        shutil.rmtree(path)
        with open('example_3_messages.json') as fp:
            response = self.c.post('/upload', {'dataset_name': 'test_dataset', 'file': fp})
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Dataset was successfully uploaded and processed.')
            self.assertTrue(os.path.exists(path))

    def tearDown(self):
        pass


class InstructionsTestCase(TestCase):
    def setUp(self):
        self.c = Client()

    def test_index_page(self):
        response = self.c.get(reverse('instructions'))
        self.assertEqual(response.status_code, 200)


class DashboardRedirectTestCase(TestCase):
    def setUp(self):
        self.c = Client()

    def test_redirect_if_not_logged_in(self):
        response = self.c.get(reverse('dashboard'))
        self.assertRedirects(response, '/login/')


class DashboardTestCase(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.c.force_login(self.user)

    def test_graph_displayed(self):
        response = self.c.get(reverse('dashboard'))

