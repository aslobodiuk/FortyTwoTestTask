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

    def test_admin_link_processing(self):
        "test correct filled lynk_type field with admin url"
        mommy.make(Request, link='/admin/qwrety/asd')
        link_type = Request.objects.first().link_type
        self.assertEqual(link_type, 3)

    def test_static_link_processing(self):
        "test correct filled lynk_type field with static url"
        mommy.make(Request, link='/static/qwrety/asd')
        link_type = Request.objects.first().link_type
        self.assertEqual(link_type, 2)

    def test_edit_link_processing(self):
        "test correct filled lynk_type field with edit url"
        mommy.make(Request, link='/edit/qwrety/asd')
        link_type = Request.objects.first().link_type
        self.assertEqual(link_type, 1)

    def test_other_link_processing(self):
        "test correct filled lynk_type field with other url"
        mommy.make(Request, link='/icnijioavboi/qwrety/asd')
        link_type = Request.objects.first().link_type
        self.assertEqual(link_type, 0)
