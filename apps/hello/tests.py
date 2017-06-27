from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from apps.hello import views


class HomeViewTest(TestCase):

    def test_home(self):
        "test for view, checking context"
        client = Client()
        response = client.get(reverse(views.home))
        c = Person.objects.first()

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

        self.assertEqual(response.context["p"].lastname, c.name)
        self.assertEqual(response.context["p"].lastname, c.lastname)
        self.assertEqual(response.context["p"].dob, c.dob)
        self.assertEqual(response.context["p"].bio, c.bio)
        self.assertEqual(response.context["p"].email, c.email)
        self.assertEqual(response.context["p"].jabber, c.jabber)
        self.assertEqual(response.context["p"].skype, c.skype)
        self.assertEqual(response.context["p"].othercontacts, c.othercontacts)

class InitialDataTest(TestCase):

    def test_model_person(self):
        "existing of initial contact data"
        self.assertTrue(Person.objects.filter(pk=1).exists())
