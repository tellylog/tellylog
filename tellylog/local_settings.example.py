"""
Django local example settings for the Tellylog project
"""

LOCAL_SETTINGS = True
from settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'security-key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS += [
    'debug_toolbar',
]

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

TVDB_API_KEY = 'api-key'
