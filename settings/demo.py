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

ALLOWED_HOSTS = ['*.talentstomorrow.com']
JWT_AUTH['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=7)
