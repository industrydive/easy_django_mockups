# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os.path
from django.conf import settings
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django.template import TemplateDoesNotExist, RequestContext
from django import template
from .models import Mockup
from django.template.base import Template
from django.template.utils import get_app_template_dirs
from pathlib import Path
from django.template.response import TemplateResponse


def display_template(request, mockup_template_name):
	# If we're in a non-development environment, BAIL EARLY
	if not settings.DEBUG:
		return HttpResponse(status=403)

	contents = None
	context = RequestContext(request, {})
	json_filename = os.path.splitext(mockup_template_name)[0]

	mock = Mockup(mockup_template_name)
	mock.read_html_file()
	html_contents = mock.contents
	if html_contents:
		template = Template(html_contents)
	else:
		return HttpResponse(status=404)


	json_stuff = mock.load_related_json(json_filename)
	if json_stuff:
		context.update(json_stuff)
	elif mock.error_message:
		messages.add_message(request, messages.ERROR, mock.error_message)
 

	try:
		return HttpResponse(template.render(context))
#		return render(request, 'mockups/' + mockup_template_name, context)
	except TemplateDoesNotExist as error:
		return HttpResponse(status=404)

