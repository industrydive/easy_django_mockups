To Install
==========
pip install easymockups
add the new module to your INSTALLED_APPS settings
add 'url(r'^', include('easymockups'))' to your root-level urls.py

This package requires you to create a 'mockups' directory inside any 'templates' directory you normally save your django templates to. Any template you put into that mockups directory can be accessed directoy via the url path /mockups/[templatename].html. Note that this only works if you have listed your own relevant apps in the INSTALLED_APPS settings.py setting.
