"""
Django settings for xnoGTD project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from dotenv import load_dotenv
from os import getenv
import dj_database_url

load_dotenv()

APP_NAME = getenv("FLY_APP_NAME")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getenv('DEBUG')
STATIC_DEBUG = getenv('STATIC_DEBUG')

ALLOWED_HOSTS = [
    f"{APP_NAME}.fly.dev",
    'localhost',
    '127.0.0.1'
]

CSRF_TRUSTED_ORIGINS = [
    f"https://{APP_NAME}.fly.dev",
]

INTERNAL_IPS = [
    "127.0.0.1",
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "debug_toolbar",
    'gtd.apps.GtdConfig',
    'api.apps.ApiConfig',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'xnoGTD.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'xnoGTD.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": getenv("DB_NAME"),
#         "USER": getenv("DB_USER"),
#         "PASSWORD": getenv("DB_PASS"),
#         "HOST": getenv("DB_HOST"),
#         "PORT": getenv("DB_PORT"),
#     }
# }
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': getenv('PGDATABASE'),
#         'USER': getenv('PGUSER'),
#         'PASSWORD': getenv('PGPASSWORD'),
#         'HOST': getenv('PGHOST'),
#         'PORT': getenv('PGPORT', 5432),
#         'OPTIONS': {
#             'sslmode': 'require',
#         },
#         'DISABLE_SERVER_SIDE_CURSORS': True,
#     }
# }

DATABASES = {
    'default': dj_database_url.config(
        default=getenv('DB_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = False

USE_TZ = False  # TODO

SHORT_DATETIME_FORMAT = "m/d/y H:i",  # '10/25/06 14:30'
DATETIME_FORMAT = "m/d/y H:i",  # '10/25/06 14:30'

DATETIME_INPUT_FORMATS = [
    "%m/%d/%y %H:%M",  # '10/25/06 14:30'
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
if STATIC_DEBUG:
    STATICFILES_DIRS = [BASE_DIR / 'data/static']
    STATIC_URL = '/static/'
else:
    STATIC_URL = '/static/'
    STATIC_ROOT = BASE_DIR / 'data/static/'

    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'data/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SESSION_COOKIE_AGE = 60 * 60 * 24 * 30
