from .base import *
from decouple import config, Csv


SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

INSTALLED_APPS += [
    'debug_toolbar',
]

INTERNAL_IPS = '127.0.0.1'

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]

DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')


DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': '',
}
