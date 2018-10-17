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


class TestDebugTrue(TestCase):
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
        print('\n\n\n\n\n\n respose body was {}'.format(resp.content.decode('utf-8')))

        # Test taht even though we remove the json file, we sill get a valid reesponse bc the HTML file still exists
        # We only test for a substring at the end of the html_contents string because the django renderer
        # should have stripped out the {{ testvar }} part during renderinng, since the json object doesnt exist any more
        os.remove(self.json_file_path)
        resp = self.client.get(self.testsuite_urlpath)
        self.assertEqual(200, resp.status_code)
        self.assertIn('exclamation points!!  </body', resp.content.decode('utf-8'))

        print('\n\n\n\n\n\n respose body was {}'.format(resp.content.decode('utf-8')))

        # Test that removing the HTML file will cause the page to 404
        os.remove(self.html_file_path)
        resp = self.client.get(self.testsuite_urlpath)
        self.assertEqual(404, resp.status_code)




class TestDebugFalse(TestCase):
    def setUp(self):
        self.filename_base='testsuitefile'
        self.html_file_path = os.path.join('easymockups', settings.MOCKUPS_DIR, '{}.html'.format(self.filename_base))
        self.json_file_path = os.path.join('easymockups', settings.MOCKUPS_DIR, '{}.json'.format(self.filename_base))
        self.testsuite_urlpath = reverse('display_template', kwargs={'mockup_template_name': 'testsuitefile.html'})


    @override_settings(DEBUG=False)
    def test403(self):
        resp = self.client.get(self.testsuite_urlpath)
        self.assertEqual(403, resp.status_code)
        self.assertNotIn('this is some test json!', resp.content.decode("utf-8"))


class TestMockupModel(TestCase):
    def setUp(self):
        pass


class TestJsonLoader(TestCase):

#    TEMPLATES = [
#        {
#            'BACKEND': 'django.template.backends.django.DjangoTemplates',
#            'DIRS': ['/templates', '/mockups'],
#            'APP_DIRS': True,
#            'OPTIONS': {
#                'context_processors': [
#                    'django.template.context_processors.debug',
#                    'django.template.context_processors.request',
#                    'django.contrib.auth.context_processors.auth',
#                    'django.contrib.messages.context_processors.messages',
#                ],
#            },
#        },
#    ]

    def setUp(self):
        pass

 #   @override_settings(TEMPLATES=TEMPLATES)
    def test_file_open(self):
        assertresults = {'testvar': 'im a testvar'}
        l = JSONLoader('/test.json')
        json_contents = l.render_json_to_string()
        self.assertEqual(assertresults, json_contents)


