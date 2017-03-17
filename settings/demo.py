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

CORS_ORIGIN_WHITELIST = (
    'https://demo.talentstomorrow.com'
)

AWS_STORAGE_BUCKET_NAME = 'static-files-asdf324fqsadkn1109fsadfbvmb64adf4af4142cknkj'
ALLOWED_HOSTS = ['*']
JWT_AUTH['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=7)
