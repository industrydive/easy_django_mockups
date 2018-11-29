import json
from django.db import models
from django import template
from django.conf import settings
from django.template import TemplateDoesNotExist
from django.template.utils import get_app_template_dirs
#from django.template.loaders.app_directories import Loader
from django.template.loaders.filesystem import Loader as FilesystemLoader
from django.template.engine import Engine
from django.apps import apps
from pathlib import Path
import os.path


if hasattr(settings, 'MOCKUPS_DIR'):
	MOCKUPS_DIR = settings.MOCKUPS_DIR
else:
	MOCKUPS_DIR = 'mockups'

if hasattr(settings, 'JSON_ERRORS_ENABLED'):
	JSON_ERRORS_ENABLED = settings.JSON_ERRORS_ENABLED
else:
	JSON_ERRORS_ENABLED = True


DIRS = getattr(settings, 'TEMPLATES', [])
dirs = [os.path.join(dir, MOCKUPS_DIR) for dir in DIRS[0]['DIRS']]

from django.template import Engine
from django.template.base import Origin


class Loader(FilesystemLoader):

    def get_dirs(self):
    	# TODO: update this to append to self.dirs, instead of overriding completely
    	if MOCKUPS_DIR:
	        return get_app_template_dirs('templates/{}'.format(MOCKUPS_DIR))
    	else:
	        return get_app_template_dirs('templates')


class Mockup(object):

	def __init__(self, mockup_template_name):
		self.json = None
		self.error_message = None

		self.engine = Engine(dirs=dirs, app_dirs=True)
		self.loader = self.engine.find_template_loader('easymockups.models.Loader')

		self.mockup_template_name = mockup_template_name
		self.html = ''


	def read_html_file(self):

		try:
			print '\n\n------\ntrying to open html file {}'.format(self.mockup_template_name)
			print 'dirs was {}'.format(self.engine.dirs)
			print 'app_dirs was {}'.format(self.engine.app_dirs)
			self.html = self.loader.get_template(self.mockup_template_name)
		except Exception as e:
			print '\n\n COULD NOT OPEN THE FILE, ERROR WAS {}'.format(e)
			self.html = ''

	def load_related_json(self, filename_base):
		try:

			loader = JSONLoader(filename_base + '.json')
			loader.load_json_to_dict()
			jsonstuff = loader.get_json()
			return jsonstuff

		except (TemplateDoesNotExist, ValueError) as e:
			if JSON_ERRORS_ENABLED:
				self.error_message = 'JSON File appears to have some problems -- {}'.format(e)


class JSONLoader(object):
	use_os_path = False
	use_template_loader = False

	def __init__(self, json_path):
		self.contents = '{}'
		self.json = {}

		paths = get_app_template_dirs('templates')
		paths += get_app_template_dirs(MOCKUPS_DIR)

		for path in paths:
			thepath = os.path.join(path, json_path)
			print '\n\n ===\ntrying to open file at {}'.format(thepath)
			try:
				with open(thepath, 'r') as f:
					self.contents = f.read()
			except Exception as e:
				continue
#			self.html = self.loader.get_template(self.mockup_template_name)


	def load_json_to_dict(self):
		self.json = json.loads(self.contents)

	def get_json(self):
		return self.json
