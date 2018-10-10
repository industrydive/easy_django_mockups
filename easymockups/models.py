import json
from django.db import models
from django import template
from django.conf import settings
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

	def create_html_file(self):
		return

	def render_associated_json_file(self, filename_base):
		js = template.loader.get_template('{}/{}.json'.format(MOCKUPS_DIR, filename_base))

		jsread = js.render()

		jsonstuff = json.loads(jsread)
		return jsonstuff
