from .dev import *


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": abspath(join(SITE_ROOT, "database", 'dev.db')),
    }
}

R_AVAILABLE = True
SECRET_KEY = 'Helluuuiiii!!!'
