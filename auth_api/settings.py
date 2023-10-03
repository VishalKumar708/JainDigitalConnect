"""
Django settings for auth_api project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
from datetime import timedelta
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-a3z&h2hki16x=vk*87!8-xba!tg!50szf=!npl0=)kpvg(_4)w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    # "debug_toolbar",
    'rest_framework_simplejwt',
    'rest_framework',
    'fcm_django',
    'jdcApi'

    # 'rest_framework.authtoken'
]

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'accounts.middleware.ValidateURLAndJSONMiddleware',

    # "debug_toolbar.middleware.DebugToolbarMiddleware",
]

# for debug the program
# INTERNAL_IPS = [
#     "127.0.0.1",
# ]
ROOT_URLCONF = 'auth_api.urls'

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

WSGI_APPLICATION = 'auth_api.wsgi.application'
# for creating custom user
AUTH_USER_MODEL = 'accounts.User'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'api',
        'USER': 'root',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = "GMT"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# *********************    SMS for otp    *****************************
SID = 'AC74f8aa592b9f4bc82af4402dfd2ce24a'
# AUTH_TOKEN = '580a9c14bfb1bc99add5ba9c820d858c'
# AUTH_TOKEN = '9bc540aefab30e0bff9d9780623866b9'
# AUTH_TOKEN = '9a76bfb5fa67140a3747eef4fd576f08'
AUTH_TOKEN = 'c5303cd7cae25ccb58cbc1a150719fbe'
SENDER_NUMBER = '+15187540316'
OTP_EXPIRY_DURATION = 600  # in seconds

# *************************    Django Logger   ****************************
# import os
LOG_DIR = os.path.join(BASE_DIR, 'log')

# Ensure the log directory exists, and create it if it doesn't
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s  %(lineno)s %(message)s",

        },
        "plain": {
            "format": "%(levelname)s: %(asctime)s | %(module)s.py| func: %(funcName)s| line number: %(lineno)s| %(message)s",

        },
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        'info': {
            "level": "INFO",
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, "info.log"),
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            "formatter": "verbose",
            "encoding": 'utf-8'
        },
        'error': {
            "level": "ERROR",
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, "error.log"),
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            "formatter": "verbose",
            "encoding": 'utf-8'
        },
        'terminal': {
            "level": "INFO",
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, "console.log"),
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            "formatter": "verbose",
            "encoding": 'utf-8'
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "terminal"],
            "propagate": False,
            "level": "INFO"
        },
        "info": {
            "handlers": ["info"],
            "propagate": False,
            "level": "INFO"
        },
        "error": {
            "handlers": ["error"],
            "level": "ERROR",
            "propagate": False,
        }

    },
    "root": {
        "handlers": ["info", "error", "console"],  # Send messages to both info and error handlers
        "level": "INFO",
    },
}

#  *******************************   Rest Framework settings   *******************************
REST_FRAMEWORK = {
    # 'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination', #for builtin pagination
    'DEFAULT_PAGINATION_CLASS': 'accounts.pagination.CustomPagination',# for customized pagination
    'PAGE_SIZE': 5,
    # 'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework_simplejwt.authentication.JWTAuthentication',),

    # help to exclude jwt authentication for some api
    'DEFAULT_AUTHENTICATION_CLASSES': ('accounts.custom_jwt_authentication.CustomJWTAuthentication',),

    'EXCEPTION_HANDLER': 'accounts.jwt_custom_exception.custom_jwt_exception_handler',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=180),  # Set your desired access token expiration time
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),  # Set your desired refresh token expiration time
    'SLIDING_TOKEN_LIFETIME': timedelta(days=1),  # Set your desired sliding token lifetime
    'SLIDING_TOKEN_REFRESH_LIFETIME_GRACE_PERIOD': timedelta(minutes=60),  # Optional
    "AUTH_HEADER_TYPES": ("Token",),
}

#  ********************************   firebase settings to send push notification   ***********************


import firebase_admin
from firebase_admin import credentials
cred = credentials.Certificate(os.path.join(BASE_DIR, 'google-services_for_JCDDev.json'))
app = firebase_admin.initialize_app(cred)

FCM_DJANGO_SETTINGS = {
     # an instance of firebase_admin.App to be used as default for all fcm-django requests
     # default: None (the default Firebase app)
    "DEFAULT_FIREBASE_APP": app,
     # default: _('FCM Django')
    "APP_VERBOSE_NAME": "FCM Notifications",
     # true if you want to have only one active device per registered user at a time
     # default: False
    "ONE_DEVICE_PER_USER": True,
     # devices to which notifications cannot be sent,
     # are deleted upon receiving error response from FCM
     # default: False
    "DELETE_INACTIVE_DEVICES": False,
}

