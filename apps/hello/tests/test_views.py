# -*- coding: utf-8 -*-
from datetime import datetime
import json
from django.test import TestCase
from model_mommy import mommy
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from apps.hello.models import Person, Request
from apps.hello import views


class HomeViewTest(TestCase):

    def setUp(self):
        self.person = mommy.make(Person)

    def test_home(self):
        "test for view, checking context, rendering to html"
        response = self.client.get(reverse(views.home))
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

    def test_data_in_template(self):
        "test if template contains data from db"
        response = self.client.get(reverse(views.home))
        c = Person.objects.first()

        self.assertContains(response, c.name)
        self.assertContains(response, c.lastname)
        self.assertContains(response, c.dob.year)
        self.assertContains(response, c.dob.month)
        self.assertContains(response, c.dob.day)
        self.assertContains(response, c.email)
        self.assertContains(response, c.jabber)
        self.assertContains(response, c.skype)


class AdminDataTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(
            username='admin',
            email='aslobodiuk@example.com',
            password='admin'
        )

    def test_adminuser(self):
        "check if initial superuser exists"

        username = 'admin'
        password = 'admin'

        u = User.objects.first()
        self.assertEqual(u.is_superuser, True)
        self.assertEqual(u.username == username, True)
        self.assertEqual(u.check_password(password), True)


class RequestViewTest(TestCase):

    def test_request(self):
        "test for view"
        response = self.client.get(reverse(views.requests))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'requests.html')
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    def test_help(self):
        "test for help view"
        response = self.client.get(reverse(views.help))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_for_last_10_requests_new(self):
        "test if view return last 10 requests"
        for i in range(10):
            Request.objects.create(link="/path/")
        for i in range(10):
            Request.objects.create(link="/help/")
        response = self.client.get(reverse(views.help))
        json_data = json.loads(response.content)

        ids = []
        for r in Request.objects.all():
            ids.append(r.id)

        self.assertEqual(len(json_data), 10)
        for i in range(10):
            self.assertEqual(json_data[i]['text'], '/help/')
            self.assertTrue(json_data[i]['id'] in ids[-10:])

    def test_for_last_requests_lt_10(self):
        "test if db has less than 10 requests"
        for i in range(5):
            Request.objects.create(link="/help/")
        response = self.client.get(reverse(views.help))
        json_data = json.loads(response.content)

        cnt = Request.objects.all().count()
        ids = []
        for r in Request.objects.all():
            ids.append(r.id)

        self.assertEqual(len(json_data), cnt)
        for i in range(cnt):
            self.assertEqual(json_data[i]['text'], '/help/')
            self.assertTrue(json_data[i]['id'] in ids[-cnt:])


class EditViewTest(TestCase):

    def setUp(self):
        self.person = mommy.make(Person)
        self.user = User.objects.create_superuser(
            username='admin',
            email='aslobodiuk@example.com',
            password='admin'
        )

    def test_initial_data_in_template(self):
        "test if template contains data from db"
        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse(views.edit))
        c = Person.objects.first()

        self.assertContains(response, c.name)
        self.assertContains(response, c.lastname)
        self.assertContains(response, c.dob.year)
        self.assertContains(response, c.dob.month)
        self.assertContains(response, c.dob.day)
        self.assertContains(response, c.email)
        self.assertContains(response, c.jabber)

    def test_django_widget(self):
        "test for datepicker widget"
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('edit'))
        self.assertContains(
            response,
            '''<input id="id_dob"'''
        )
        self.assertContains(
            response,
            '''{dateFormat: 'yy-mm-dd', changeYear: true, yearRange: '-50:'}'''
        )

    def test_auth(self):
        "test auth"
        response = self.client.get(reverse('edit'))
        self.assertEqual(response.status_code, 302)
        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse('edit'))
        self.assertEqual(response.status_code, 200)

    def test_ajax_form_with_fail_context(self):
        "wrong context"
        self.client.login(username='admin', password='admin')

        fail_context_em_bio = {
            'name': 'Vasya',
            'lastname': 'Pupkin',
            'dob': '1994-09-15',
            'email': 'aslobodascasm',
            'jabber': 'alex@42cc.com',
            'bio': 'bio' * 100,
        }
        response = self.client.post(reverse('edit'), fail_context_em_bio)
        self.assertContains(response, "error")
        self.assertContains(response, "Max length 140 characters!")
        self.assertContains(response, 'Enter a valid email')

        fail_context_jab_other = {
            'name': 'Vasya',
            'lastname': 'Pupkin',
            'dob': '1994-09-15',
            'email': 'aslobodiuk@gmail.com',
            'jabber': 'alexsdac',
            'bio': 'bio',
            'othercontacts': 'othercontacts' * 100
        }
        response = self.client.post(reverse('edit'), fail_context_jab_other)
        self.assertContains(response, "error")
        self.assertContains(response, "Max length 140 characters!")
        self.assertContains(response, 'Enter a valid email')

    def test_ajax_form_with_right_context(self):
        "right context"
        self.client.login(username='admin', password='admin')
        context = {
            'name': 'Vasya',
            'lastname': 'Pupkin',
            'dob': '1994-09-15',
            'email': 'aslobodiuk@gmail.com',
            'jabber': 'asdsd@42cc.com',
            'bio': 'fasfasf',
            'othercontacts': 'asdfwec',
        }
        response = self.client.post(reverse('edit'), context)
        self.assertContains(response, "success")

    def test_right_post_data(self):
        "right post data"
        self.client.login(username='admin', password='admin')
        context = {
            'name': 'Vasya',
            'lastname': 'Pupkin',
            'dob': '1994-09-15',
            'email': 'aslobodiuk@gmail.com',
            'jabber': 'asdsd@42cc.com',
            'bio': 'fasfasf',
            'othercontacts': 'asdfwec',
        }
        self.client.post(reverse('edit'), context)
        p = Person.objects.first()
        self.assertEqual(p.name, context["name"])
        self.assertEqual(p.lastname, context["lastname"])
        self.assertEqual(
            p.dob,
            datetime.strptime(context["dob"], "%Y-%m-%d").date()
        )
        self.assertEqual(p.email, context["email"])
        self.assertEqual(p.jabber, context["jabber"])
        self.assertEqual(p.bio, context["bio"])
        self.assertEqual(p.othercontacts, context["othercontacts"])

    def test_with_wrong_post_data(self):
        "wrong post data"
        self.client.login(username='admin', password='admin')
        p = Person.objects.first()
        context = {
            'name': 'Vasya',
            'lastname': 'Pupkin',
            'dob': '1994-09-15',
            'email': 'aasdasdom',
            'jabber': 'asdwedwedom',
            'bio': 'fasfasf' * 100,
            'othercontacts': 'asdfwec' * 100,
        }
        self.client.post(reverse('edit'), context)
        new = Person.objects.first()
        self.assertEqual(p.name, new.name)
        self.assertEqual(p.lastname, new.lastname)
        self.assertEqual(p.dob, new.dob)
        self.assertEqual(p.email, new.email)
        self.assertEqual(p.photo, new.photo)
        self.assertEqual(p.jabber, new.jabber)
        self.assertEqual(p.bio, new.bio)
        self.assertEqual(p.othercontacts, new.othercontacts)
