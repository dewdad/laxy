"""
Django settings for laxy project.

Generated by 'django-admin startproject' using Django 1.11.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
import logging

import os
from datetime import timedelta
import tempfile
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured
import environ

from laxy.utils import get_secret_key

logger = logging.getLogger(__name__)

APP_ENV_PREFIX = 'LAXY_'


class PrefixedEnv(environ.Env):
    """
    Like environ.Env, except it adds the given prefix to the keys of each
    default environment variable specified upon instantiation.

    This means you can omit the prefix everywhere in settings.py /
    default_settings.py, but use the prefix in .env and actual environment
    variables.
    """

    def __init__(self, prefix, **scheme):
        # Add prefix to dictionary keys
        self.scheme = dict([('%s%s' % (prefix, k), v)
                            for k, v in scheme.items()])


# Build paths inside the project like this: app_root.path('templates')
app_root = environ.Path(__file__) - 2
BASE_DIR = str(app_root)
envfile = app_root.path('.env')
environ.Env.read_env(envfile())  # read the .env file

default_env = PrefixedEnv(
    APP_ENV_PREFIX,
    DEBUG=(bool, False),
    ADMIN_EMAIL=(str, None),
    ADMIN_USERNAME=(str, None),
    AWS_ACCESS_KEY_ID=(str, None),
    AWS_SECRET_ACCESS_KEY=(str, None),
    DEFAULT_COMPUTE_RESOURCE=(str, 'default'),
    ALLOWED_HOSTS=(list, ['*']),
    BROKER_URL=(str, 'amqp://'),
    EMAIL_HOST_URL=('email_url', ''),
    EMAIL_HOST_USER=(str, ''),
    EMAIL_HOST_PASSWORD=(str, ''),
    STATIC_ROOT=(str, str(app_root.path('static')())),
    STATIC_URL=(str, '/static/'),
    MEDIA_ROOT=(str, str(app_root.path('uploads')())),
    MEDIA_URL=(str, 'uploads/'),
    FILE_CACHE_PATH=(str, tempfile.gettempdir()),
)


def env(env_key=None, default=environ.Env.NOTSET):
    return default_env('%s%s' % (APP_ENV_PREFIX, env_key), default=default)


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ADMIN_EMAIL = env('ADMIN_EMAIL')
ADMIN_USERNAME = env('ADMIN_USERNAME')
if ADMIN_EMAIL and ADMIN_USERNAME:
    ADMINS = [(ADMIN_USERNAME, ADMIN_EMAIL)]

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')

AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')

DEFAULT_COMPUTE_RESOURCE = env('DEFAULT_COMPUTE_RESOURCE')

FILE_CACHE_PATH = env('FILE_CACHE_PATH')

ALLOWED_HOSTS = env('ALLOWED_HOSTS')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'it0!1vg87mhmvos$e#+9^2g4z6my1=np5^cnxr6#+**54hi(q%'

try:
    SECRET_KEY = env('SECRET_KEY')
except ImproperlyConfigured:
    SECRET_KEY = get_secret_key()

# SECRET_KEY = get_secret_key()

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': default_env.db('%sDATABASE_URL' % APP_ENV_PREFIX,
                              default='postgres:///postgres:postgres@db:5432')
}

SITE_ID = 1

BROKER_URL = env('BROKER_URL')
CELERY_RESULT_BACKEND = 'django-db'
# CELERY_RESULT_BACKEND = 'db+postgresql://postgres:postgres@db:5432/postgres'
# CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
# CELERY_RESULT_BACKEND = BROKER_URL
# if DEBUG:
#     CELERY_ALWAYS_EAGER = True
#     logger.warning("CELERY_ALWAYS_EAGER = True
#                     seems to prevent tasks from starting ?")
# CELERY_IGNORE_RESULT = True

MEDIA_ROOT = str(env('MEDIA_ROOT'))
MEDIA_URL = str(env('MEDIA_URL'))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_URL = str(env('STATIC_URL'))
STATIC_ROOT = str(env('STATIC_ROOT'))

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_extensions',
    'django_celery_results',
    'django_celery_beat',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'drf_openapi',
    'reversion',
    'storages',
    # 'laxy_backend.apps.LaxyBackendConfig',
    'laxy_backend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'laxy.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [app_root.path('templates')]
        ,
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

# https://github.com/ottoyiu/django-cors-headers#configuration
# CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = ('localhost:8002',
                         'erc.monash.edu',
                         'erc.monash.edu.au',
                         '118.138.240.175:8002',
                         )
# CSRF_TRUSTED_ORIGINS = ('localhost:8000',)

REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.AllowAny',
        # 'rest_framework.permissions.IsAdminUser',
        'rest_framework.permissions.IsAuthenticated',
        # Use Django's standard `django.contrib.auth` permissions,
        # or allow read-only access for unauthenticated users.
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    # http://www.django-rest-framework.org/api-guide/pagination/#cursorpagination
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.CursorPagination',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# TODO: Apparently drf_openapi doesn't honor this setting.
#       File an issue ? Query on gitter chat ?
# SWAGGER_SETTINGS = {'SECURITY_DEFINITIONS': {
#     'basic': {'type': 'basic'}},
#     'api_key': {
#         'type': 'apiKey',
#         'name': 'api_key',
#         'in': 'header'
#     }
# }
# '''
# Used as extra information to generate the OpenAPI documentation / schema.
#
# These should match the authentication types available
# (eg from REST_FRAMEWORK.DEFAULT_AUTHENTICATION_CLASSES)
#
# See https://django-rest-swagger.readthedocs.io/en/latest/settings/ and
# https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#security-definitions-object
# '''

WSGI_APPLICATION = 'laxy.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

_pwlib = 'django.contrib.auth.password_validation.'
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': _pwlib + 'UserAttributeSimilarityValidator',
    },
    {
        'NAME': _pwlib + 'MinimumLengthValidator',
    },
    {
        'NAME': _pwlib + 'CommonPasswordValidator',
    },
    {
        'NAME': _pwlib + 'NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

JWT_AUTH = {
    # 'JWT_ENCODE_HANDLER':
    # 'rest_framework_jwt.utils.jwt_encode_handler',
    #
    # 'JWT_DECODE_HANDLER':
    # 'rest_framework_jwt.utils.jwt_decode_handler',
    #
    # 'JWT_PAYLOAD_HANDLER':
    # 'rest_framework_jwt.utils.jwt_payload_handler',
    #
    # 'JWT_PAYLOAD_GET_USER_ID_HANDLER':
    # 'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',
    #
    # 'JWT_PAYLOAD_GET_USERNAME_HANDLER':
    # 'rest_framework_jwt.utils.jwt_get_username_from_payload_handler',

    # 'JWT_RESPONSE_PAYLOAD_HANDLER':
    # 'rest_framework_jwt.utils.jwt_response_payload_handler',

    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_ALGORITHM': 'HS256',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': timedelta(days=4),
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,

    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=7),

    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
}
'''
See https://getblimp.github.io/django-rest-framework-jwt/
'''
