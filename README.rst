# easy_django_mockups
A library to allow for easy mockups using the power of Django templates


To Install
==========
clone this repo to somewhere on your computer. 

``virtualenv venv``

``source venv/bin/activate``

``pip install -r requirements.txt``

``python setup.py sdist``

After the above commands are run, you should have a tar.gz file under the dist/ directory. From there, pip install this package into your django project by running the following command, replacing PATH/TO/ with whatever path leads to the easymockups-0.1.tar.gz file.

``pip install PATH/TO/dist/easymockups-0.1.tar.gz``

Then add the new module to your INSTALLED_APPS settings, and add 

``url(r'^', include('easymockups'))``

to your root-level urls.py

From there, you'll need to create a 'mockups' directory inside any 'templates' directory you normally save your django templates to. Any template you put into that mockups directory can be accessed directoy via the url path /mockups/[templatename].html, where [templatename] is the name of the file you just created. You can also add a JSON file that follows the same naming pattern and the template should include the json objects as primitive mock django models.


