# -*- coding: utf-8 -*-
from django.test import TestCase

from .models import Person, Change


class HttpTest(TestCase):

    def test_signal_processor(self):
        "test for signal, add data to change model"
        p = Person(
            name='Vasya',
            lastname='Pupkin',
            dob='1994-09-15',
            email='aslobodiuk@gmail.com',
            jabber='asdsd@42cc.com',
            bio='fasfasf',
            othercontacts='asdfwec'
        )
        p.save()
        ch = Change.objects.order_by('-time')[0]
        self.assertEqual(ch.status, 'C')
        self.assertEqual(ch.model.lower(), 'person')
        self.assertEqual(ch.object, u'%s' % p.pk)
        p.first_name = 'Ivan'
        p.save()
        ch = Change.objects.order_by('-time')[0]
        self.assertEqual(ch.status, 'U')
        p.delete()
        ch = Change.objects.order_by('-time')[0]
        self.assertEqual(ch.status, 'D')
