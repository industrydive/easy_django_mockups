# easy_django_mockups
A library to allow for easy mockups using the power of Django templates


To Install
==========
``pip install easy-django-mockups``

Then add the new module to your INSTALLED_APPS settings, and add 

``url(r'^', include('easymockups'))``

to your root-level urls.py's urlpatterns.

From there, you'll need to create a 'mockups' directory inside any 'templates' directory you normally save your django templates to. Any template you put into that mockups directory can be accessed directoy via the url path /mockups/[templatename].html, where [templatename] is the name of the file you just created. You can also add a JSON file that follows the same naming pattern and the template should include the json objects as primitive mock django models.


