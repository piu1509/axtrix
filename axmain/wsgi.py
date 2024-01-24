"""
WSGI config for axmain project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
from decouple import config
from django.core.wsgi import get_wsgi_application

DEBUG = config('DEBUG', default=True, cast=bool)

if DEBUG:
    os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE',
        'axmain.settings.development')
else:
    os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE',
        'axmain.settings.production')

application = get_wsgi_application()
