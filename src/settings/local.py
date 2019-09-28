from settings.common import *

# NOTE: Most of the  following settings are just for demo purposes.

# Set to True so that no extra CDN service needs to be run in order to
# serve media files. It shall be disabled in the prod environment.
DEBUG = True
ALLOWED_HOSTS = ['*']

# In a real prod env shall be kept secret, not stored in the settings.
SECRET_KEY = 'fpiq&_efd55lw&t+nfv&d=)htud*%ch-k2jremd0mje#aso&pt'

# SQLite to make development testing more comfortable and quicker.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '..', 'db.sqlite3'),
    }
}


# Just for a demo purposes, e.g. some CDN should be used instead.
STATIC_ROOT = os.path.join(BASE_DIR, 'src/static')
MEDIA_ROOT = os.path.join(STATIC_ROOT, 'src/media')
MEDIA_URL = '/media/'

CORS_ORIGIN_REGEX_WHITELIST = [
    r'^https://\w+\.herokuapp\.com$'
]
