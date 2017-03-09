from .dev import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tottest',
        'USER': 'test',
        'PASSWORD': 'test123',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

R_AVAILABLE = True
SECRET_KEY = 'Helluuuiiii!!!'
