# -*- coding: utf-8 -*-
from django.test import TestCase
from model_mommy import mommy
from django.template import Template, Context, TemplateSyntaxError

from apps.hello.models import Person


class TemplateTagTest(TestCase):
    def setUp(self):
        self.person = mommy.make(Person)

    def test_template_tag_edit_link(self):
        "test for rendering edit_link tag"
        t = Template('{% load hello_extras %}{% edit_link person %}')
        c = Context({'person': self.person})
        rendered = t.render(c)
        self.assertEqual(
            rendered,
            u'<a href="/admin/hello/person/1/">Edit (admin)</a>'
            )

    def test(self):
        "test for arguments in edit_link tag"
        c = Context({'person': self.person})

        def render(t): return Template(t).render(c)

        self.assertRaises(
            TemplateSyntaxError,
            render,
            '{% load hello_extras %}{% edit_link person asdasdsd %}'
            )
        self.assertRaises(
            TemplateSyntaxError,
            render,
            '{% load hello_extras %}{% edit_link %}'
            )
        self.assertRaises(
            TemplateSyntaxError,
            render,
            '{% load hello_extras %}{% edit_link qwerty %}'
            )
