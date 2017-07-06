# -*- coding: utf-8 -*-
import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from model_mommy import mommy

from apps.hello.models import Person, Request
from apps.hello import views


class PersonModelTest(TestCase):

    def setUp(self):
        self.person = mommy.make(Person)

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

    def test_unicode_in_db(self):
        "test сyrillic in db"
        p = Person.objects.first()
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
        req = Request(link="/requests/")
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
