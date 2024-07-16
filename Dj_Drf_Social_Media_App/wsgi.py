"""
WSGI config for Dj_Drf_Social_Media_App project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Dj_Drf_Social_Media_App.settings')

application = get_wsgi_application()
