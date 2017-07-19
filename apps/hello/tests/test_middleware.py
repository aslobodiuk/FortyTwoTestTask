# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from model_mommy import mommy

from apps.hello.models import Request, Person
from apps.hello import views


class MiddlewareTests(TestCase):

    def setUp(self):
        self.person = mommy.make(Person)

    def test_request_processing(self):
        "test middleware for input data in model"
        response = self.client.get(reverse(views.home))
        count = Request.objects.all().count()
        link = Request.objects.first().link

        self.assertEqual(response.status_code, 200)
        self.assertEqual(count, 1)
        self.assertEqual(link, reverse(views.home))

    def test_admin_link_processing(self):
        "test correct filled lynk_type field with admin url"
        self.client.get('/admin/qwrety/asd')
        link_type = Request.objects.first().link_type
        self.assertEqual(link_type, 3)

    def test_static_link_processing(self):
        "test correct filled lynk_type field with static url"
        self.client.get('/static/qwrety/asd')
        link_type = Request.objects.first().link_type
        self.assertEqual(link_type, 2)

    def test_edit_link_processing(self):
        "test correct filled lynk_type field with edit url"
        self.client.get('/edit/qwrety/asd')
        link_type = Request.objects.first().link_type
        self.assertEqual(link_type, 1)

    def test_other_link_processing(self):
        "test correct filled lynk_type field with other url"
        self.client.get('/asdfwc/qwrety/asd')
        link_type = Request.objects.first().link_type
        self.assertEqual(link_type, 0)
