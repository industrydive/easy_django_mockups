import json
from django.db import models
from django import template
from django.conf import settings
from django.template import TemplateDoesNotExist

# Create your models here.

if hasattr(settings, 'MOCKUPS_DIR'):
	MOCKUPS_DIR = settings.MOCKUPS_DIR
else:
	MOCKUPS_DIR = 'mockups'

if hasattr(settings, 'JSON_ERRORS_ENABLED'):
	JSON_ERRORS_ENABLED = settings.JSON_ERRORS_ENABLED
else:
	JSON_ERRORS_ENABLED = True


class Mockup(object):

	def __init__(self):
		self.json = None
		self.error_message = None

	def create_html_file(self):
		return

	def load_related_json(self, filename_base):
		try:
			js = template.loader.get_template('{}/{}.json'.format(MOCKUPS_DIR, filename_base))
			jsread = js.render()
			jsonstuff = json.loads(jsread)
			self.json = jsonstuff
		except (TemplateDoesNotExist, ValueError) as e:
			self.error_message = 'JSON File appears to have some problems -- {}'.format(e)

