import sys
from os.path import abspath, join, dirname

# Paths
PROJECT_ROOT = abspath(join(dirname(__file__), '..', '..'))
SITE_ROOT = abspath(join(PROJECT_ROOT, '..'))

sys.path.insert(0, abspath(join(PROJECT_ROOT, "third_party")))
sys.path.insert(0, abspath(join(PROJECT_ROOT, 'apps')))
sys.path.insert(0, abspath(join(PROJECT_ROOT, '..',)))

# Static files (CSS, JavaScript, Images)
LOCALE_PATHS = [abspath(join(PROJECT_ROOT, 'locale'))]
MEDIA_ROOT = join(PROJECT_ROOT, 'site_media', 'media')
STATIC_ROOT = join(PROJECT_ROOT, 'site_media', 'static')
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATICFILES_DIRS = [
    join(PROJECT_ROOT, 'static'),
]

STATICI18N_ROOT = STATICFILES_DIRS[0]

