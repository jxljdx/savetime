"""
WSGI config for savetime project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""
import sys
import site
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "savetime.settings")

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/var/www/virtualEnvs/savetimesite/lib/python2.7/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/var/www/virtualEnvs/savetimesite/savetime')
sys.path.append('/var/www/virtualEnvs/savetimesite/savetime/savetimeapp')

# Activate your virtual env
activate_env=os.path.expanduser("/var/www/virtualEnvs/savetimesite/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
