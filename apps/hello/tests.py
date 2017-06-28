from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from . import views
from .models import Person, Request


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

        u = User.objects.first()
        self.assertEqual(u.is_superuser, True)
        self.assertEqual(u.username == username, True)
        self.assertEqual(u.check_password(password), True)

    def test_model_person(self):
        "existing of initial contact data"
        self.assertTrue(Person.objects.filter(pk=1).exists())


class RequestViewTest(TestCase):

    def test_request(self):
        "test for view"
        client = Client()
        response = client.get(reverse(views.requests))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'requests.html')

    def test_help(self):
        "test for help view"
        client = Client()
        response = client.get(reverse(views.help))

        self.assertEqual(response.status_code, 200)


class RequestModelTest(TestCase):

    def test_string_representation(self):
        "test string representations"
        req = Request(link="/requests/")
        self.assertEqual(str(req), req.link)


class MiddlewareTests(TestCase):

    def test_requestProcessing(self):
        "test middleware for input data in model"
        client = Client()
        response = client.get(reverse(views.home))
        count = Request.objects.all().count()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(count, 1)
