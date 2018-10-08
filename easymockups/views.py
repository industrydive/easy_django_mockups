# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os.path
from django.conf import settings
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django import template


if hasattr(settings, 'MOCKUPS_DIR'):
	MOCKUPS_DIR = settings.MOCKUPS_DIR
else:
	MOCKUPS_DIR = 'mockups'

def display_template(request, mockup_template_name):
	if not settings.DEBUG:
		return HttpResponse(status=403)

	context = {}
	json_filename = os.path.splitext(mockup_template_name)[0]

	try:
		js = template.loader.get_template('{}/{}.json'.format(MOCKUPS_DIR, json_filename))

		jsread = js.render()

		jsonstuff = json.loads(jsread)
		context.update(jsonstuff)

	except Exception as e:
		error_message = 'JSON File appears to have some problems -- {}'.format(e)
		messages.add_message(request, messages.ERROR, error_message)
 	
	return render(request, '{}/{}'.format(MOCKUPS_DIR, mockup_template_name), context)

