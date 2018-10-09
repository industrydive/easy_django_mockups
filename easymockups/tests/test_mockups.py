#from unittest import TestCase
import django
from django.conf import settings
from django.test import TestCase, Client
from easymockups.views import display_template
import test_settings
from django.urls import reverse
import os.path
from django.template import TemplateDoesNotExist

django.setup()


class TestResponseValid(TestCase):
    def setUp(self):
        self.client = Client()



    def test_200_response(self):
        getreq = self.client.get(reverse('display_template', kwargs={'mockup_template_name': 'test.html'}))
        self.assertEqual(200, getreq.status_code)


class TestFileCreation(TestCase):
    def setUp(self):
        pass

    def test_create_file(self):
        filename='testsuitefile.html'
        file_contents = '<html><body>Hello! Im a test file made for the test suite!!</body></html>'
        file_path = os.path.join('easymockups', settings.MOCKUPS_DIR, filename)

        with open(file_path, 'w') as f:
            f.write(file_contents)

        testsuite_reverse = reverse('display_template', kwargs={'mockup_template_name': 'testsuitefile.html'})

        getreq = self.client.get(testsuite_reverse)
        self.assertEqual(200, getreq.status_code)

        os.remove(file_path)

        resp = self.client.get(testsuite_reverse)
        
        self.assertEqual(404, resp.status_code)



class TestFileLocation(TestCase):
    def setUp(self):
        pass

    def test_found_file(self):
        pass