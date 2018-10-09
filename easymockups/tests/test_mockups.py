#from unittest import TestCase
import django
from django.conf import settings
from django.test import TestCase, Client
from easymockups.views import display_template
import test_settings
from django.urls import reverse

#if not settings.configured:
#    settings.configure(default_settings=test_settings, DEBUG=True)
django.setup()
#settings.configure()

class TestJoke(TestCase):
    def setUp(self):
        self.client = Client()



    def test_is_string(self):
        s = 'hi'

        getreq = self.client.get(reverse('display_template', kwargs={'mockup_template_name': 'test.html'}))
        self.assertEqual(200, getreq.status_code)