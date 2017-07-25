# -*- coding: utf-8 -*-
from django.test import TestCase
from model_mommy import mommy

from apps.hello.models import Person, Request


class PersonModelTest(TestCase):

    def test_string_representation(self):
        "test string representations"
        p = mommy.make(Person)
        self.assertEqual(str(p), p.name + ' ' + p.lastname)


class RequestModelTest(TestCase):

    def test_string_representation(self):
        "test string representations"
        req = mommy.make(Request)
        self.assertEqual(str(req), req.link)
