from .common import *

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = ['.zmrenwu.com']
DEBUG = False

# django anymail grid
ANYMAIL = {
    "SENDGRID_API_KEY": "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",
    # "MAILGUN_SENDER_DOMAIN": 'mg.example.com',
}
EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
DEFAULT_FROM_EMAIL = "zmrenwu_blog@zmrenwu.com"
