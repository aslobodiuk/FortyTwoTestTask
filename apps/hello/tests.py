from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from .models import Person, Request
from . import views


class HomeViewTest(TestCase):
    fixtures = ['initial.json']

    def test_home(self):
        "test for view, checking context, rendering to html"
        client = Client()
        response = client.get(reverse(views.home))
        c = Person.objects.first()

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

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

        username = 'admin'
        password = 'admin'

        u = User.objects.first()
        self.assertEqual(u.is_superuser, True)
        self.assertEqual(u.username == username, True)
        self.assertEqual(u.check_password(password), True)


class PersonModelTest(TestCase):
    fixtures = ['initial.json']

    def test_string_representation(self):
        "test string representations"
        p = Person.objects.first()
        self.assertEqual(str(p), p.name + ' ' + p.lastname)

    def test_model_person(self):
        "existing of initial contact data"
        self.assertTrue(Person.objects.filter(pk=1).exists())

    def test_model_el_cnt(self):
        "testing empty, or 2+ elements in DB"
        self.assertEqual(Person.objects.all().count(), 1)


class RequestViewTest(TestCase):

    def test_request(self):
        "test for view"
        client = Client()
        response = client.get(reverse(views.requests))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'requests.html')
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    def test_help(self):
        "test for help view"
        client = Client()
        response = client.get(reverse(views.help))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')


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


class EditViewTest(TestCase):
    fixtures = ['initial.json']

    def test_django_widget(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('edit'))
        self.assertContains(response,
                            u'''<input class="datepicker" id="id_dob"''')
        self.assertContains(response,
                            u'''{dateFormat: 'yy-mm-dd', changeYear: true, yearRange: '-50:'}''')
