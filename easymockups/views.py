# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os.path
from django.conf import settings
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django import template



def display_template(request, mockup_template_name):
	if not settings.DEBUG:
		return HttpResponse(status=403)
	context = {}
	json_filename = os.path.splitext(mockup_template_name)[0]

	try:
		js = template.loader.get_template('mockups/{}.json'.format(json_filename))

		jsread = js.render()

		jsonstuff = json.loads(jsread)
		context.update(jsonstuff)

	except Exception as e:
		error_message = 'JSON File appears to have some problems -- {}'.format(e)
		messages.add_message(request, messages.ERROR, error_message)
 	
	return render(request, 'mockups/' + mockup_template_name, context)

