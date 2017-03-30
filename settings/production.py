import os
from .base import *  # noqa

ALLOWED_HOSTS = ['*.talentstomorrow.com']
JWT_AUTH['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=7)

OPBEAT = {
    'ORGANIZATION_ID': 'fab3fd138af14d0e8f2b4ad7efcd22ce',
    'APP_ID': '18d9e6610c',
    'SECRET_TOKEN': '6799043939c43b57c3721338afd5b808fb88ec0a',
}

