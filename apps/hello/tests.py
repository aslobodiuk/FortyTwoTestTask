from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from apps.hello import views


class HomeViewTest(TestCase):

    def test_home(self):
        "test for view"
        client = Client()
        response = client.get(reverse(views.home))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
