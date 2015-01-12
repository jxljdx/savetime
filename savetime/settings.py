"""
Django settings for savetime project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import socket

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '91s=j%np)cwtt-3i@e!uzo)(#0-$yyy7ih4a_7q+62@i=2o&jd'

'''
FIXME:
We should branch off base on production server's condition, so multiple dev
servers can share the same dev settings, for instance,
if (is production server's hostname):
    production server's settings
else:
    dev server's settings
'''
if (socket.gethostname() == "com.host.dev"):
    DEBUG = True
    TEMPLATE_DEBUG = True

    # Database
    # https://docs.djangoproject.com/en/1.7/ref/settings/#databases
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'test',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '3306'
            # 'ENGINE': 'django.db.backends.sqlite3',
            # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

    ALLOWED_HOSTS = []
else:
    DEBUG = False
    TEMPLATE_DEBUG = False

    # Database
    # https://docs.djangoproject.com/en/1.7/ref/settings/#databases
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'savetime',
            'USER': 'dbmaster',
            'PASSWORD': '5uperAwesome',
            'HOST': 'rdsr3ijmyr3ijmy.mysql.rds.aliyuncs.com',
            'PORT': '3306'
            # 'ENGINE': 'django.db.backends.sqlite3',
            # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

    ALLOWED_HOSTS = [
        # '182.92.176.72'
        '*'
    ]

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'savetimeapp'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'savetime.urls'

WSGI_APPLICATION = 'savetime.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'zh-CN'

# TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

# App specific static files are all located in directory named "static" within
# the app, no need specify these static directories' pathes, since django by
# default knows where to find them. To add static files at project level,
# provide the path here.
STATICFILES_DIRS = ()

FILE_CHARSET = 'utf-8'
DEFAULT_CHARSET = 'utf-8'
