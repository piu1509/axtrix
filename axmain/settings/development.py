from .base import *
from .mailer import *
from datetime import timedelta
from decouple import config, Csv

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

INSTALLED_APPS += [
    'debug_toolbar',
]

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


# Debug Toolbar Configurations
# ----------------------------
INTERNAL_IPS = '127.0.0.1'

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]

DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': '',
}



# CORS Settings - Development
# ---------------------------

# CORS_ALLOW_CREDENTIALS = config('CORS_ALLOW_CREDENTIALS', default=False, cast=bool)

CORS_ORIGIN_ALLOW_ALL = config('CORS_ORIGIN_ALLOW_ALL', default=False, cast=bool)

CORS_ORIGIN_WHITELIST = config('CORS_ORIGIN_WHITELIST_HOSTS', cast=Csv())


# SIMPLE_JWT - Development
# ---------------------------
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=180),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# CELERY Settings - Development
# -----------------------------
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Berlin'

ZOOM_API_KEY = config('ZOOM_API_KEY')
ZOOM_API_SECRET = config('ZOOM_API_SECRET')

# Logging Settings - Development
# ------------------------------
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': True,
#     'formatters': {
#         'verbose': {
#             'format': '%(levelname)s %(asctime)s %(message)s'
#             # 'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
#         },
#         'simple': {
#             'format': '%(levelname)s %(message)s'
#         },
#     },
#     'handlers': {
#         'console': {
#             'level': 'WARNING',
#             'class': 'logging.StreamHandler',
#             'formatter': 'simple'
#         },
#     },
#     'loggers': {
#         'daphne': {
#             'handlers': ['console'],
#             'level': 'DEBUG'
#         },
#         'stream_framework': {
#             'handlers': ['console'],
#             'level': 'WARNING',
#             'filters': []
#         },
#         'redis': {
#             'handlers': ['console'],
#             'level': 'WARNING',
#             'filters': []
#         },
#         '': {
#             'handlers': [],
#             'level': 'WARNING',
#             'filters': []
#         },
#     }
# }
