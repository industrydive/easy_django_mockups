import json
from django.db import models
from django import template
from django.conf import settings
from django.template import Origin, TemplateDoesNotExist
from django.template.utils import get_app_template_dirs
#from django.template.loaders.app_directories import Loader
from django.template.loaders.filesystem import Loader as FilesystemLoader
from django.template.loaders.base import Loader as BaseLoader
from django.template.engine import Engine
from django.apps import apps
import os.path
from django.template import Origin, TemplateDoesNotExist
from django.utils._os import safe_join

if hasattr(settings, 'MOCKUPS_DIR'):
	MOCKUPS_DIR = settings.MOCKUPS_DIR
else:
	MOCKUPS_DIR = 'mockups'

if hasattr(settings, 'JSON_ERRORS_ENABLED'):
	JSON_ERRORS_ENABLED = settings.JSON_ERRORS_ENABLED
else:
	JSON_ERRORS_ENABLED = True

from django.template import Engine
from django.template.base import Origin


class Loader(BaseLoader):

	def get_contents(self, origin):
		# print 'TRYING TO GET_CONTENTS()'
		try:
			with open(origin.name) as fp:
				return fp.read()
		except IOError:#FileNotFoundError:
			raise TemplateDoesNotExist(origin)
		except Exception as e:
			pass
			# print 'HIT THE EXCEPTION IN GET_CONTENTS IN LOADER'
			# print 'exception was, ', e


	def get_template_sources(self, template_name):
		"""
		Return an Origin object pointing to an absolute path in each directory
		in template_dirs. For security reasons, if a path doesn't lie inside
		one of the template_dirs it is excluded from the result set.
		"""
		if hasattr(self, 'dirs') and self.dirs is not None:
			dirs = self.dirs
		else:
			dirs = self.engine.dirs


		# print 'DIRS IN GET_TEMPLATE_SOURCES() IS, ', dirs
		for template_dir in dirs:
			try:
				name = safe_join(template_dir, template_name)
			except SuspiciousFileOperation:
				# The joined path was located outside of this template_dir
				# (it might be inside another one, so this isn't fatal).
				continue
			yield Origin(
				name=name,
				template_name=template_name,
				loader=self,
			)


class Mockup(object):

	def __init__(self, mockup_template_name):
		self.json = None
		self.error_message = None


		TEMPLATE_DIRS = getattr(settings, 'TEMPLATES', [])
		dirs = [os.path.join(dir, MOCKUPS_DIR) for dir in TEMPLATE_DIRS[0]['DIRS']]

		# THis turns out to be the key. We are manually finding out which dirs to pass to Engine
		# which lets get_template_sources() find the templates correctly. could probably override
		# get_template_sources() to find better templates
		self.engine = Engine(dirs=dirs, app_dirs=True)
		self.loader = self.engine.find_template_loader('easymockups.models.Loader')

		self.mockup_template_name = mockup_template_name
		self.template_obj = None



	def read_html_file(self):
		'''
		This basically is a wrapper that calls the associated loader's get_template() method, and sets 
		a property called 'template_obj', which we can then use to render inside a view.
		'''
		try:
			self.template_obj = self.loader.get_template(self.mockup_template_name)
		except Exception as e:
			self.template_obj = None

	def load_related_json(self, filename_base):
		json_string = '{}'

		try:
			for origin in self.loader.get_template_sources(filename_base + '.json'):
				try:
					json_string = self.loader.get_contents(origin)
				except Exception as e:
					# print 'Exception in load_related_json was {}'.format(e)
					pass
			jsonstuff = json.loads(json_string)
			return jsonstuff

		except (TemplateDoesNotExist, ValueError) as e:
			if JSON_ERRORS_ENABLED:
				self.error_message = 'JSON File appears to have some problems -- {}'.format(e)

