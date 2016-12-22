import os
from .base import *  # noqa

INSTALLED_APPS.append('debug_toolbar')

DEBUG = True

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

CORS_ORIGIN_WHITELIST = (
    'localhost:3000'
)
