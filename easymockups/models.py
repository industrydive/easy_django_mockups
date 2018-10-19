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


if hasattr(settings, 'MOCKUPS_DIR'):
	MOCKUPS_DIR = settings.MOCKUPS_DIR
else:
	MOCKUPS_DIR = 'mockups'

if hasattr(settings, 'JSON_ERRORS_ENABLED'):
	JSON_ERRORS_ENABLED = settings.JSON_ERRORS_ENABLED
else:
	JSON_ERRORS_ENABLED = True


class Mockup(object):

	def __init__(self, mockup_template_name):
		self.json = None
		self.error_message = None
		self.contents = None

		self.paths = get_app_template_dirs('templates')
		self.paths += get_app_template_dirs(MOCKUPS_DIR)
		self.mockup_template_name = mockup_template_name


	def read_html_file(self):
		for path in self.paths:
			thepath = Path(path, 'mockups', self.mockup_template_name)
			try:
				with open(thepath, 'r') as f:
					self.contents = f.read()
			except FileNotFoundError as e:
				continue

#		return self.contents


	def load_related_json(self, filename_base):
		try:

			loader = JSONLoader(filename_base + '.json')
			jsonstuff = loader.load_json_to_dict()
			return jsonstuff

		except (TemplateDoesNotExist, ValueError) as e:
			if JSON_ERRORS_ENABLED:
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
				continue


	def load_json_to_dict(self):

		return json.loads(self.contents)





