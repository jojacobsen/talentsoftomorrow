import os
from .base import *  # noqa

JWT_AUTH['JWT_EXPIRATION_DELTA'] = datetime.timedelta(hours=8)

CORS_ORIGIN_ALLOW_ALL = True
ALLOWED_HOSTS = ['*']
AWS_STORAGE_BUCKET_NAME = 'static-files-asdf324fqsadkn1109fsadfbvmb64adf4af4142cknkj'

DEBUG = True
