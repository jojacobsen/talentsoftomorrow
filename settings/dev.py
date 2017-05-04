import os
from .base import *  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tot-db',
        'USER': 'test',
        'PASSWORD': 'test123',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

JWT_AUTH['JWT_EXPIRATION_DELTA'] = datetime.timedelta(hours=8)

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True

INSTALLED_APPS.append('debug_toolbar')
INSTALLED_APPS.append('rosetta')

MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

INTERNAL_IPS = ['127.0.0.1']

DEBUG = True
