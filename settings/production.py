import os
from .base import *  # noqa

JWT_AUTH['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=7)
