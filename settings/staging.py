import os
from .base import *  # noqa

JWT_AUTH['JWT_EXPIRATION_DELTA'] = datetime.timedelta(hours=8)

CORS_ORIGIN_ALLOW_ALL = True

DEBUG = True
