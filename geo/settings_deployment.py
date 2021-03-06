"""
Django settings for geo project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

from django.utils.log import DEFAULT_LOGGING

from .settings_shared import *

SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    from .secrets import SECRET_KEY # should throw an error in production if secretkey is not present

POSTGIS_PASSWORD = os.environ.get("POSTGIS_PASSWORD")
if not POSTGIS_PASSWORD:
    from .secrets import POSTGIS_PASSWORD

POSTGIS_HOST = os.environ.get("POSTGIS_HOST") or "localhost"
POSTGIS_PORT = os.environ.get("POSTGIS_PORT") or ""
POSTGIS_USER = os.environ.get("POSTGIS_USER") or "postgres"
POSTGIS_NAME = os.environ.get("POSTGIS_NAME") or "postgres"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["edtgeodata.edtinc.net", "geo.trevor-sullivan.tech", "geoprod.trevor-sullivan.tech", "localhost"]

ADMINS = [("Trevor", 'trevor@trevor-sullivan.tech')]
MANAGERS = ADMINS

# SERVER_EMAIL = 'django@trevor-sullivan.tech'

# Application definition


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': POSTGIS_NAME,
        'USER': POSTGIS_USER,
        'PASSWORD': POSTGIS_PASSWORD,
        "HOST": POSTGIS_HOST,
        "PORT": POSTGIS_PORT,
    }
}

EMAIL_BACKEND= 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.office365.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'geodata@edtinc.net'
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
if not EMAIL_HOST_PASSWORD:
    from .secrets import EMAIL_HOST_PASSWORD

DEFAULT_LOGGING['handlers']['console']['filters'] = [] # disables default console logging, allowing gunicorn to see them
#might regret this, look here for more https://stackoverflow.com/questions/38131255/logging-and-email-not-working-for-django-for-500
DEFAULT_LOGGING['loggers'][''] = {
    'handlers': ['console', 'mail_admins'],
    'level': 'INFO',
    'propagate': True
}


