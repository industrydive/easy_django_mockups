#from unittest import TestCase
import django
from django.conf import settings
from django.test import TestCase, Client
from easymockups.views import display_template
import test_settings
from django.urls import reverse
import os.path
from django.template import TemplateDoesNotExist
import json

django.setup()


class TestFileCreation(TestCase):
    def setUp(self):
        self.filename_base='testsuitefile'
        self.html_file_path = os.path.join('easymockups', settings.MOCKUPS_DIR, '{}.html'.format(self.filename_base))
        self.json_file_path = os.path.join('easymockups', settings.MOCKUPS_DIR, '{}.json'.format(self.filename_base))
        self.testsuite_urlpath = reverse('display_template', kwargs={'mockup_template_name': 'testsuitefile.html'})

    def test_create_file(self):


        with open(self.html_file_path, 'w') as f:
            html_contents = """
                <html><body>We should see the output from "testvar" in the json file 
                below after the exclamation points!! {{ testvar }} </body></html>
                """
            f.write(html_contents)

        with open(self.json_file_path, 'w') as f:
            json.dump({"testvar": "this is some test json!"}, f)


        # Test the template renderinng works with the json file we created in the above lines
        resp = self.client.get(self.testsuite_urlpath)
        self.assertEqual(200, resp.status_code)
        self.assertIn('this is some test json!', resp.content.decode("utf-8"))


        # Test taht even though we remove the json file, we sill get a valid reesponse bc the HTML file still exists
        # We only test for a substring at the end of the html_contents string because the django renderer
        # should have stripped out the {{ testvar }} part during renderinng, since the json object doesnt exist any more
        os.remove(self.json_file_path)
        resp = self.client.get(self.testsuite_urlpath)
        self.assertEqual(200, resp.status_code)
        self.assertIn('exclamation points!!  </body', resp.content.decode('utf-8'))


        # Test that removing the HTML file will cause the page to 404
        os.remove(self.html_file_path)
        resp = self.client.get(self.testsuite_urlpath)
        self.assertEqual(404, resp.status_code)

