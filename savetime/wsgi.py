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

SITE_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir(os.path.join(SITE_ROOT, "lib", "python2.7", "site-packages"))

# Add the app's directory to the PYTHONPATH
sys.path.append(os.path.join(SITE_ROOT, "savetime"))
sys.path.append(os.path.join(SITE_ROOT, "savetime", "savetimeapp"))

# Activate your virtual env
activate_env=os.path.expanduser(os.path.join(SITE_ROOT, "bin", "activate_this.py"))
execfile(activate_env, dict(__file__=activate_env))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()