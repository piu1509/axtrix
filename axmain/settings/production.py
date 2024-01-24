from .base import *
from .mailer import *
from datetime import timedelta
from decouple import config, Csv


SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

INSTALLED_APPS += []

# Database Default Postgres12
# ----------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # 'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}


# CORS Settings - Production
# --------------------------
# CORS_ALLOW_CREDENTIALS = config('CORS_ALLOW_CREDENTIALS', default=False, cast=bool)

CORS_ORIGIN_ALLOW_ALL = config('CORS_ORIGIN_ALLOW_ALL', default=False, cast=bool)

CORS_ORIGIN_WHITELIST = config('CORS_ORIGIN_WHITELIST_HOSTS', cast=Csv())


# SIMPLE_JWT - Development
# ------------------------
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}