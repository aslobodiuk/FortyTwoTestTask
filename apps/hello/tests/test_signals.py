# -*- coding: utf-8 -*-
from django.test import TestCase
from model_mommy import mommy
from apps.hello.models import Person, Change


class SignalTest(TestCase):

    def setUp(self):
        self.person = mommy.make(Person)

    def test_signal_object_creation(self):
        "test for creating db entry about object creation"
        ch = Change.objects.order_by('-time')[0]
        self.assertEqual(ch.status, 'C')
        self.assertEqual(ch.model.lower(), 'person')
        self.assertEqual(ch.object, u'%s' % self.person.pk)

    def test_signal_object_editing(self):
        "test for creating db entry about object editing"
        self.person.first_name = 'Ivan'
        self.person.save()
        ch = Change.objects.order_by('-time')[0]
        self.assertEqual(ch.status, 'U')

    def test_signal_object_deletion(self):
        "test for creating db entry about object deletion"
        self.person.delete()
        ch = Change.objects.order_by('-time')[0]
        self.assertEqual(ch.status, 'D')
