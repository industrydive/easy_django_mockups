# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os.path
from django.conf import settings
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse



def display_template(request, mockup_template_name):
	if not settings.DEBUG:
		return HttpResponse(status=403)
	context = {}
	json_filename = os.path.splitext(mockup_template_name)[0]

	print('\n\n\n template_name is {}'.format(mockup_template_name))
	print('\n\n\n path is {}'.format(os.path.abspath('.')))
	json_file = os.path.abspath('{}/mockups/jsondata/{}.json'.format(settings.BASE_DIR, json_filename))
	print('\n\n\nJSON FILE IS {}'.format(json_file))
	try:
		with open(json_file, 'r') as opened_file:
			jsonstuff = json.load(opened_file)
			context.update(jsonstuff)
	except Exception as e:
		error_message = 'JSON File appears to have some problems -- {}'.format(e)
		messages.add_message(request, messages.ERROR, error_message)
 	
	return render(request, 'mockups/' + mockup_template_name, context)

