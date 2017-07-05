# -*- coding: utf-8 -*-
from StringIO import StringIO
from django.test import TestCase
from django.db import models
from django.core.management import call_command


class CommandTest(TestCase):

	def test_command(self):
		"test printmodel command"
        content = StringIO()
        call_command("printmodels", stdout=content)
        content.seek(0)
        all_models = models.get_models()
        out = content.read()
        for model in all_models:
            self.assertIn(model.__name__, out)
            self.assertIn(str(model.objects.all().count()), out)