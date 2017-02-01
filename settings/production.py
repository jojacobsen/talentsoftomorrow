import os
from .base import *  # noqa

ALLOWED_HOSTS = ['*.talentstomorrow.com']
JWT_AUTH['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=7)
