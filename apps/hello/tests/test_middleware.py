# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from model_mommy import mommy

from apps.hello.models import Request, Person
from apps.hello import views


class MiddlewareTests(TestCase):

    def setUp(self):
        self.person = mommy.make(Person)

    def test_requestProcessing(self):
        "test middleware for input data in model"
        response = self.client.get(reverse(views.home))
        count = Request.objects.all().count()
        link = Request.objects.first().link

        self.assertEqual(response.status_code, 200)
        self.assertEqual(count, 1)
        self.assertEqual(link, reverse(views.home))
