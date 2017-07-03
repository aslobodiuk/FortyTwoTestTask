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
        "existing of initial Person data"
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

    def test_edit(self):
        self.user = User.objects.create_user(
            username='vadim', email='vadimanikin1@gmail.com', password='qwerty')
        response = self.client.post(reverse('edit'))
        self.assertEqual(response.status_code, 302)
        self.client.login(username='vadim', password='qwerty')
        response = self.client.get(reverse('edit'))
        self.assertEqual(response.status_code, 200)
        p = Person.objects.filter().reverse()[0]
        response = self.client.get(reverse('home'))
        self.assertContains(response, p.name)
        self.assertContains(response, p.lastname)
        self.assertContains(response, p.dob.year)
        self.assertContains(response, p.dob.month)
        self.assertContains(response, p.dob.day)
        self.assertContains(response, p.bio)
        self.assertContains(response, p.email)
        self.assertContains(response, p.jabber)
        self.assertContains(response, p.skype)
        self.assertContains(response, p.othercontacts)
        context = {
            'name': 'Jhon',
            'lastname': 'Smith',
            'dob': '1993-12-31',
            'bio': 'unique',
        }
        self.client.post(reverse('edit'), context)
        response = self.client.get(reverse('home'))
        cont = Person.objects.filter().reverse()[0]
        self.assertContains(response, cont.dob.day)
        self.assertContains(response, cont.dob.month)
        self.assertContains(response, cont.dob.year)
        del context['dob']
        for key in context.keys():
            self.assertEqual(cont[key], context[key])
        fail_context = {
            'name': 'Vasya',
            'lastname': 'Pupkin',
            'dob': '15/09/1994',
            'bio': 'fasfasf',
            'jabber': 'aasdsd',
            'email': 'asdasqwe',
            'bio': 'bio' * 100,
        }
        response = self.client.post(reverse('edit'), fail_context)
        self.assertContains(response, u'Enter a valid Jabber ID.')
        self.assertContains(response, u'Enter a valid email')
        self.assertContains(response, "Max length 140 characters!")
        response = self.client.get(reverse('home'))
        for key in fail_context.keys():
            self.assertNotContains(response, fail_context[key])

    def test_ajax_form(self):
        self.client.login(username='admin', password='admin')
        fail_context = {
            'name': 'Vasya',
            'lastname': 'Pupkin',
            'dob': '1994-09-15',
        }
        response = self.client.post(reverse('edit'), fail_context)
        self.assertContains(response, "error")
        context = {
            'name': 'Vasya',
            'lastname': 'Pupkin',
            'dob': '1994-09-15',
            'bio': 'fasfasf',
        }
        response = self.client.post(reverse('edit'), context)
        self.assertContains(response, "success")
