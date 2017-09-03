from .common import *

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY',
                            default='i3k%m-808v3_)^h7975iw4v&fl5chq41^19j@u+b*vx7dvw*q$')

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
# django anymail grid
# ANYMAIL = {
#     "SENDGRID_API_KEY": "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",
#     # "MAILGUN_SENDER_DOMAIN": 'mg.example.com',
# }
# EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
# DEFAULT_FROM_EMAIL = "zmrenwu_blog@zmrenwu.com"
