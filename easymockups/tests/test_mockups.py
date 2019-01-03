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
from unittest import skip


django.setup()
filename_base='testsuitefile'
second_filename_base='testsuitenojsonfile'
BASE_DIR = ''
MOCKUPS_DIR = getattr(settings, 'MOCKUPS_DIR', '')

DIRS = getattr(settings, 'TEMPLATES', [])
dirs = [os.path.join(dir, MOCKUPS_DIR) for dir in DIRS[0]['DIRS']]


html_file_path = os.path.join(dirs[0], '{}.html'.format(filename_base))
json_file_path = os.path.join(dirs[0], '{}.json'.format(filename_base))

second_html_file_path = os.path.join(dirs[0], '{}.html'.format(second_filename_base))

bad_html_file_path = os.path.join(dirs[0], '{}.html'.format('nofile'))
print 'in test_mockups.py, html_file_path is, ', html_file_path



class TestDebugTrue(TestCase):
    def setUp(self):
        self.testsuite_urlpath = reverse('display_template', kwargs={'mockup_template_name': 'testsuitefile.html'})
        self.second_testsuite_urlpath = reverse('display_template', kwargs={'mockup_template_name': 'testsuitenojsonfile.html'})
        self.bad_testsuite_urlpath = reverse('display_template', kwargs={'mockup_template_name': 'nofile.html'})

    @skip
    def test_response_200_with_json(self):
        # Test the template renderinng works with the json file we created in the above lines
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
        # Test that removing the HTML file will cause the page to 404
        resp = self.client.get(self.bad_testsuite_urlpath)
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

    @skip
    def test_file_open(self):
        assertresults = {'testvar': 'this is some test json!'}
        l = JSONLoader('testsuitefile.json')
        l.load_json_to_dict()
        json_contents = l.get_json()
        self.assertEqual(assertresults, json_contents)

#        print '\n\n\n html file path is {}'.format(html_file_path)
