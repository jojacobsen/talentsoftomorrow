import os

from .settings import *  # noqa


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'circle_test',
        'USER': 'ubuntu',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

SECRET_KEY = 'Helluuuiiii!!!'
