import os
from .settings import *  # noqa

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

CORS_ORIGIN_WHITELIST = (
    'localhost:3000'
)
