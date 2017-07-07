# -*- coding: utf-8 -*-
import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from model_mommy import mommy

from apps.hello.models import Person, Request
from apps.hello import views


class PersonModelTest(TestCase):

    def test_string_representation(self):
        "test string representations"
        p = mommy.make(Person)
        self.assertEqual(str(p), p.name + ' ' + p.lastname)

    def test_two_elements_in_db(self):
        "testing 2 elements in DB rendering first element in home view"
        p1 = mommy.make(Person)
        p2 = mommy.make(Person)

        response = self.client.get(reverse(views.home))

        self.assertEqual(response.context["p"], p1)
        self.assertNotEqual(response.context["p"], p2)

        self.assertContains(response, p1.name)
        self.assertContains(response, p1.lastname)
        self.assertContains(response, p1.dob.year)
        self.assertContains(response, p1.dob.month)
        self.assertContains(response, p1.dob.day)
        self.assertContains(response, p1.email)
        self.assertContains(response, p1.jabber)
        self.assertContains(response, p1.skype)

    def test_empty_db(self):
        "return 404 if db is empty"
        response = self.client.get(reverse(views.home))
        self.assertEqual(response.status_code, 404)

    def test_unicode_in_db(self):
        "test сyrillic in db"
        p = mommy.make(Person)
        p.name = u"Алексей"
        p.lastname = u"Слободюк"
        p.save()

        response = self.client.get(reverse(views.home))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["p"].name, u"Алексей")
        self.assertEqual(response.context["p"].lastname, u"Слободюк")
        self.assertContains(response, u"Алексей")
        self.assertContains(response, u"Слободюк")


class RequestModelTest(TestCase):

    def test_string_representation(self):
        "test string representations"
        req = mommy.make(Request)
        self.assertEqual(str(req), req.link)

    def test_unicode_in_db(self):
        "test сyrillic in db"
        cyrillic_path = u"/тест/"
        response = self.client.get(cyrillic_path)
        response = self.client.get(reverse(views.help))
        json_data = json.loads(response.content)
        response_path = filter(lambda r: r["id"] == 1, json_data)[0]["link"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_path, cyrillic_path)
