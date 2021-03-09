"""
Django settings for server project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import datetime
import sys

from server.configs import Databases

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$+%$*+x%$g#+@4%a*0^)oew9rewz)n-&=cd&-yh0fzjh2=vh(d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',

    'debug_toolbar',

    'rest_framework',
    'corsheaders',
    'django_filters',
    'import_export',
    'wkhtmltopdf',
    'rest_framework_swagger',
    'rest_framework.authtoken',

    'users',
    'companies',
    'accounts',
    'wares',
    'sanads',
    'transactions',
    'cheques',
    'factors',
    'reports',
    'home',
    'imprests',

    'sobhan_admin',

    '_dashtbashi',

    'distributions',

]

ALLOWED_HOSTS = ['*']

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'corsheaders.middleware.CorsMiddleware',

    'helpers.middlewares.modify_request_middleware.ModifyRequestMiddleware',

    'helpers.middlewares.check_token_expiration.CheckTokenExpiration',

    'debug_toolbar.middleware.DebugToolbarMiddleware',

]

ROOT_URLCONF = 'server.urls'

CORS_ORIGIN_ALLOW_ALL = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'server.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = Databases

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'fa-ir'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'helpers.exception_handlers.custom_exception_handler',
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'helpers.auth.TokenAuthSupportQueryString',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
        'rest_framework.filters.SearchFilter',
    ),
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.ScopedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'verification_code': '5/hours',
    },
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'helpers.parser.NestedMultipartParser'
    ]
}

STATIC_ROOT = os.path.join(BASE_DIR, "static/")
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
MEDIA_URL = '/media/'

AUTH_USER_MODEL = 'users.User'

TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

INTERNAL_IPS = [
    # '127.0.0.1',
    # '185.239.105.10'
]

# DEBUG_TOOLBAR_CONFIG = {
#     "SHOW_TOOLBAR_CALLBACK": lambda request: True,
# }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '{}/debug.log'.format(BASE_DIR),
        },
        'inventory': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '{}/inventory.log'.format(BASE_DIR),
        },
        'tmp_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '{}/debug-tmp.log'.format(BASE_DIR),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'inventory': {
            'handlers': ['inventory'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'tmp': {
            'handlers': ['tmp_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
