import json
from django.db import models
from django import template
from django.conf import settings
from django.template import TemplateDoesNotExist
from django.template.utils import get_app_template_dirs
from django.template.loaders.app_directories import Loader
from django.template.engine import Engine
from django.apps import apps
from pathlib import Path

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

			loader = JSONLoader(filename_base + '.json')
			jsonstuff = loader.render_json_to_string()
			return jsonstuff

		except (TemplateDoesNotExist, ValueError) as e:
			self.error_message = 'JSON File appears to have some problems -- {}'.format(e)


class JSONLoader(object):
	use_os_path = False
	use_template_loader = False

	def __init__(self, json_path):
		self.contents = '{}'

		paths = get_app_template_dirs('templates')
		paths += get_app_template_dirs(MOCKUPS_DIR)

		for path in paths:
			thepath = Path(path, 'mockups', json_path)
			try:
				with open(thepath, 'r') as f:
					self.contents = f.read()
			except FileNotFoundError as e:
				print('could not openn(thepath, r), exceptoin was {}\n==================='.format(e))
				continue


	def render_json_to_string(self):

		return json.loads(self.contents)





