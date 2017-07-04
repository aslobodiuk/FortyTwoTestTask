# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import Request
from . import views


class MiddlewareTests(TestCase):

    def test_requestProcessing(self):
        "test middleware for input data in model"
        response = self.client.get(reverse(views.home))
        count = Request.objects.all().count()
        link = Request.objects.first().link

        self.assertEqual(response.status_code, 200)
        self.assertEqual(count, 1)
        self.assertEqual(link, reverse(views.home))
