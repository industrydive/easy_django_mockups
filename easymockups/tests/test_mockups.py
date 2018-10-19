#from unittest import TestCase
import django
from django.conf import settings
from django.test import TestCase, Client, override_settings
from easymockups.views import display_template
import test_settings
from django.urls import reverse
import os.path
from django.template import TemplateDoesNotExist
import json
from easymockups.models import Mockup, JSONLoader
from django.apps import apps

django.setup()
filename_base='testsuitefile'
html_file_path = os.path.join('easymockups', 'mockups', settings.MOCKUPS_DIR, '{}.html'.format(filename_base))
json_file_path = os.path.join('easymockups','mockups', settings.MOCKUPS_DIR, '{}.json'.format(filename_base))


class TestDebugTrue(TestCase):
    def setUp(self):
        self.testsuite_urlpath = reverse('display_template', kwargs={'mockup_template_name': 'testsuitefile.html'})

        with open(html_file_path, 'w') as f:
            html_contents = """
                <html><body>We should see the output from "testvar" in the json file 
                below after the exclamation points!! {{ testvar }} </body></html>
                """
            f.write(html_contents)

        with open(json_file_path, 'w') as f:
            json.dump({"testvar": "this is some test json!"}, f)




    def test_response_200_with_json(self):
        # Test the template renderinng works with the json file we created in the above lines
        print('\n\n\ntestsuite_urlpath is {}'.format(self.testsuite_urlpath))
        resp = self.client.get(self.testsuite_urlpath)
        self.assertEqual(200, resp.status_code)
        self.assertIn('this is some test json!', resp.content.decode("utf-8"))


    def test_remove_json_file(self):
        # Test taht even though we remove the json file, we sill get a valid reesponse bc the HTML file still exists
        # We only test for a substring at the end of the html_contents string because the django renderer
        # should have stripped out the {{ testvar }} part during renderinng, since the json object doesnt exist any more
        os.remove(json_file_path)
        resp = self.client.get(self.testsuite_urlpath)
        self.assertEqual(200, resp.status_code)
        self.assertIn('exclamation points!!  </body', resp.content.decode('utf-8'))


    def test_no_html_file(self):
        # Test that removing the HTML file will cause the page to 404
        os.remove(html_file_path)
        resp = self.client.get(self.testsuite_urlpath)
        self.assertEqual(404, resp.status_code)


    @override_settings(DEBUG=False)
    def test_debug_false_403(self):
        resp = self.client.get(self.testsuite_urlpath)
        self.assertEqual(403, resp.status_code)
        self.assertNotIn('this is some test json!', resp.content.decode("utf-8"))


class TestMockupModel(TestCase):
    def setUp(self):
        pass


class TestJsonLoader(TestCase):
    def setUp(self):
        with open(json_file_path, 'w') as f:
            json.dump({"testvar": "this is some test json!"}, f)

    def test_file_open(self):
        assertresults = {'testvar': 'this is some test json!'}
        l = JSONLoader('testsuitefile.json')
        json_contents = l.load_json_to_dict()
        self.assertEqual(assertresults, json_contents)


