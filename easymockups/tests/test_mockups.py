#from unittest import TestCase
import django
from django.conf import settings
from django.test import TestCase, Client, override_settings
from easymockups.views import display_template
import test_settings
from django.urls import reverse
import os.path
from django.template import TemplateDoesNotExist, Context
import json
from easymockups.models import Mockup
from django.apps import apps
from unittest import skip


django.setup()
filename_base='testsuitefile'
second_filename_base='testsuitenojsonfile'


class TestDebugTrue(TestCase):
    def setUp(self):
        self.testsuite_urlpath = reverse('display_template', kwargs={'mockup_template_name': 'testsuitefile.html'})
        self.second_testsuite_urlpath = reverse('display_template', kwargs={'mockup_template_name': 'testsuitenojsonfile.html'})
        self.bad_testsuite_urlpath = reverse('display_template', kwargs={'mockup_template_name': 'nofile.html'})

    def test_response_200_with_json(self):
        # Test the template renderinng works with the json file we have by the same name as the html file passed to the url
        resp = self.client.get(self.testsuite_urlpath)
        self.assertEqual(200, resp.status_code)
        self.assertIn('this is some test json!', resp.content.decode("utf-8"))

    def test_no_json_file(self):
        # Test taht even though we have no json file, we sill get a valid reesponse bc the HTML file still exists
        # We only test for a substring at the end of the html_contents string because the django renderer
        # should have stripped out the {{ testvar }} part during renderinng, since the json object doesnt exist any more
        resp = self.client.get(self.second_testsuite_urlpath)
        self.assertEqual(200, resp.status_code)
        self.assertIn('exclamation points!!  \n</body', resp.content.decode('utf-8'))

    def test_no_html_file(self):
        # Test that not having an HTML file by the name of the value passed into the url will cause the page to 404
        resp = self.client.get(self.bad_testsuite_urlpath)
        self.assertEqual(404, resp.status_code)

    @override_settings(DEBUG=False)
    def test_debug_false_403(self):
        resp = self.client.get(self.testsuite_urlpath)
        self.assertEqual(403, resp.status_code)
        self.assertNotIn('this is some test json!', resp.content.decode("utf-8"))


class TestMockupModel(TestCase):
    def setUp(self):
        self.mock = Mockup(filename_base + '.html')

    def test_sets_template_obj(self):
        # this should set mock.template_obj to an instance of a django Template model
        self.mock.read_html_file()
        self.assertIsNotNone(self.mock.template_obj)

    def test_render_template_works(self):
        context = Context({})
        self.mock.read_html_file()
        self.assertIn('the exclamation points!!  \n</body', self.mock.template_obj.render(context))

    def test_json_loading_works(self):
        self.mock.load_related_json(filename_base)
        self.assertEqual({"testvar": "this is some test json!"}, self.mock.json)
