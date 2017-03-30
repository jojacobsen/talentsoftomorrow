import os
from .base import *  # noqa

JWT_AUTH['JWT_EXPIRATION_DELTA'] = datetime.timedelta(hours=8)

CORS_ORIGIN_ALLOW_ALL = True
ALLOWED_HOSTS = ['*']
AWS_STORAGE_BUCKET_NAME = 'static-files-asdf324fqsadkn1109fsadfbvmb64adf4af4142cknkj'

DEBUG = True

OPBEAT = {
    'ORGANIZATION_ID': 'fab3fd138af14d0e8f2b4ad7efcd22ce',
    'APP_ID': '5ea801dc6e',
    'SECRET_TOKEN': '6799043939c43b57c3721338afd5b808fb88ec0a',
}

