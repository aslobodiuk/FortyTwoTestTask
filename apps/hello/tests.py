from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from . import views
from .models import Person


class HomeViewTest(TestCase):
    fixtures = ['initial.json']

    def test_home(self):
        "test for view, checking context"
        client = Client()
        response = client.get(reverse(views.home))
        c = Person.objects.first()

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

        self.assertEqual(response.context["p"].name, c.name)
        self.assertEqual(response.context["p"].lastname, c.lastname)
        self.assertEqual(response.context["p"].dob, c.dob)
        self.assertEqual(response.context["p"].bio, c.bio)
        self.assertEqual(response.context["p"].email, c.email)
        self.assertEqual(response.context["p"].jabber, c.jabber)
        self.assertEqual(response.context["p"].skype, c.skype)
        self.assertEqual(response.context["p"].othercontacts, c.othercontacts)


class InitialDataTest(TestCase):
    fixtures = ['initial.json']

    def test_adminuser(self):
        "check if initial superuser exists"

        username = 'alex'
        password = 'Gfhfdjpbr19`'

        u = User.objects.get(pk=1)
        self.assertEqual(u.is_superuser, True)
        self.assertEqual(u.username == username, True)
        self.assertEqual(u.check_password(password), True)

    def test_model_person(self):
        "existing of initial contact data"
        self.assertTrue(Person.objects.filter(pk=1).exists())
