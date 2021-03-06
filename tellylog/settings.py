"""
Django settings for tellylog project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!


SECRET_KEY = os.environ['SECRET_KEY']
NOCAPTCHA = True


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!

if 'DEBUG' in os.environ:
    DEBUG = os.environ['DEBUG']
else:
    DEBUG = False


def show_toolbar(request):
    return os.environ['DEBUG']

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
}


RECAPTCHA_PUBLIC_KEY = os.environ['RECAPTCHA_PUBLIC_KEY']
RECAPTCHA_PRIVATE_KEY = os.environ['RECAPTCHA_PRIVATE_KEY']

if DEBUG:
    INTERNAL_IPS = ['0.0.0.0', '127.0.0.1', '10.6.6.6']


ALLOWED_HOSTS = ['*', ]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'watson',
    'tv',
    'search',
    'tmdbcall',
    'captcha',
    'user',
    'main',
    'watchlog',
    'watchlist',

]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tellylog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'templates/',
            'override_templates/',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tellylog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

if 'TRAVIS' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'test_tellylog',
            'USER': 'postgres',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ['PG_NAME'],
            'USER': os.environ['PG_USER'],
            'PASSWORD': os.environ['PG_PASSWORD'],
            'HOST': os.environ['PG_HOST'],
            'PORT': os.environ['PG_PORT'],
            'TEST': {
                'NAME': 'test',
                'USER': 'test',
                'PASSWORD': 'test',
            },
        }
    }


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': ('django.contrib.'
                 'auth.password_validation.UserAttributeSimilarityValidator'),
    },
    {
        'NAME': ('django.contrib.'
                 'auth.password_validation.MinimumLengthValidator'),
    },
    {
        'NAME': ('django.contrib.'
                 'auth.password_validation.CommonPasswordValidator'),
    },
    {
        'NAME': ('django.contrib.'
                 'auth.password_validation.NumericPasswordValidator'),
    },
]

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
)
# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Vienna'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
"""
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ['GMAIL_ADDRESS']
EMAIL_HOST_PASSWORD = os.environ['GMAIL_PW']
DEFAULT_FROM_EMAIL = os.environ['GMAIL_ADDRESS']
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
"""
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025



STATIC_URL = '/static/'

# Media ROOT
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Media URL

MEDIA_URL = '/media/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]



LOGIN_URL = '/user/sign-in/'
# if user is not logged in, this is the URL to which they are redirected

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# does exactly what it sounds like


# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s"
            "[%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'tellylog.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'WARNING',
        },
    }
}

# Celery

BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_ACCEPT_CONTENT = ['pickle']
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_TIMEZONE = 'Europe/Vienna'
CELERY_ENABLE_UTC = True

# Redis

REDIS = {
    'HOST': '127.0.0.0.1',
    'PORT': 6379,
    'DB': 0,
}
