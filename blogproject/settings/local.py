from .common import *

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY',
                            default='i3k%m-808v3_)^hl5chq44@u+b*q1^vx7dvw*q$1^19&fl5ch194vj')

DEBUG = True

# debug toolbar
INTERNAL_IPS = ['127.0.0.1']
JQUERY_URL = ''

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INSTALLED_APPS += [
    'debug_toolbar',
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
