# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os.path
from django.conf import settings
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django.template import TemplateDoesNotExist
from django import template
from .models import Mockup

# TODO: maybe move this to something in the settings file where we retrieve the user's settings
# Maybe think about something more like DDT: https://github.com/jazzband/django-debug-toolbar/blob/master/debug_toolbar/settings.py
if hasattr(settings, 'MOCKUPS_DIR'):
	MOCKUPS_DIR = settings.MOCKUPS_DIR
else:
	MOCKUPS_DIR = 'mockups'

if hasattr(settings, 'JSON_ERRORS_ENABLED'):
	JSON_ERRORS_ENABLED = settings.JSON_ERRORS_ENABLED
else:
	JSON_ERRORS_ENABLED = True

def display_template(request, mockup_template_name):
	# If we're in a non-development environment, BAIL EARLY
	if not settings.DEBUG:
		return HttpResponse(status=403)

	context = {}
	json_filename = os.path.splitext(mockup_template_name)[0]

	mock = Mockup()
	json_stuff = mock.load_related_json(json_filename)

	if json_stuff:
		context.update(json_stuff)
	elif mock.error_message and JSON_ERRORS_ENABLED:
		messages.add_message(request, messages.ERROR, mock.error_message)
 
	try:
		return render(request, '{}/{}'.format(MOCKUPS_DIR, mockup_template_name), context)
	except TemplateDoesNotExist as error:
		return HttpResponse(status=404)

