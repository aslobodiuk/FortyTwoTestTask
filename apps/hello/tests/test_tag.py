# -*- coding: utf-8 -*-
from django.test import TestCase
from model_mommy import mommy
from django.template import Template, Context, TemplateSyntaxError

from apps.hello.models import Person


class TemplateTagTest(TestCase):

    def setUp(self):
        self.person = mommy.make(Person)
        self.c = Context({'person': self.person})

    def render(self, t, c): return Template(t).render(c)

    def test_template_tag_edit_link(self):
        "test for rendering edit_link tag"
        t = '{% load hello_extras %}{% edit_link person %}'
        self.assertEqual(
            self.render(t, self.c),
            u'<a href="/admin/hello/person/1/">Edit (admin)</a>'
            )

    def test_template_tag_edit_link_arguments(self):
        "test for incorrect arguments in edit_link tag"
        self.assertRaises(
            TemplateSyntaxError,
            self.render,
            '{% load hello_extras %}{% edit_link person asdasdsd %}',
            self.c
            )
        self.assertRaises(
            TemplateSyntaxError,
            self.render,
            '{% load hello_extras %}{% edit_link %}',
            self.c
            )
        self.assertRaises(
            TemplateSyntaxError,
            self.render,
            '{% load hello_extras %}{% edit_link qwerty %}',
            self.c
            )
