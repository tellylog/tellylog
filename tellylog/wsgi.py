"""
WSGI config for tellylog project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import dotenv

dotenv.read_dotenv(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '../.env'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tellylog.settings")

application = get_wsgi_application()
