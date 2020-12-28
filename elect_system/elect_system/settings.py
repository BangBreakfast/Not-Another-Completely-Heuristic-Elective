"""
Django settings for elect_system project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
from enum import Enum

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd@a(qr#9g9u_g40gt*nn=g#yh6!ibkcq$1_ow-bt87sy0=s#8#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
  	'user',
    'django_apscheduler',
    'course',
    'phase',
    'election'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware', 
]

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = [
    'http://127.0.0.1:8080',
    'http://localhost:8080'
]


CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)

ROOT_URLCONF = 'elect_system.urls'

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

WSGI_APPLICATION = 'elect_system.wsgi.application'
APPEND_SLASH = False

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'elective',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': 'zzzzzz',
        'TEST': {
            'CHARSET': 'utf8',
            'COLLATION': 'utf8_general_ci'
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

BASE_LOG_DIR = os.path.join(BASE_DIR, "log")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {  # Detailed logs printed into log file
            'format': '%(asctime)s [%(levelname)s] [%(threadName)s] [task_id:%(name)s] [%(filename)s:%(lineno)d]'
                      ' %(message)s'
        },
        'simple': {		# Simple logs printed on console
            'format': '%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s'
        },
    },

    'filters': {
        'require_debug_true': {  # print logs only if debug=True
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },

    'handlers': {
        'console': {			# Simple logs printed on console
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'default': {
            'level': 'INFO',  # Do not put DEBUG logs in file
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_LOG_DIR, "info.log"),
            'maxBytes': 1024 * 1024 * 50,  # 50MB
            'backupCount': 3,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
    },

    'loggers': {
        '': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
EMAIL_USE_TLS = False
EMAIL_HOST_USER = 'pku_elective@163.com'
EMAIL_HOST_PASSWORD = 'xxxxxxxx'

DEFAULT_CHARSET = 'utf-8'


class ERR_TYPE:
    INVALID_METHOD = 'Invalid method'
    JSON_ERR = 'Json format error'
    PARAM_ERR = 'Wrong parameters'
    AUTH_FAIL = 'Authentication failed'
    USER_DUP = 'This user already exists'
    USER_404 = 'This user does not exist'
    NOT_ALLOWED = 'User is not allowed to perform this operation'
    PHASE_ERR = 'Election is closed now'
    ELE_DUP = 'Duplicate election'
    ELE_404 = 'This election does not exists'
    ELE_FAIL = 'Election fails'
    COURSE_DUP = 'This course already exists'
    COURSE_404 = 'This course does not exists'
    WP_ERR = 'Invalid willing point'
    CRED_ERR = 'Your credit excceeds limit'
    TIME_CONF = 'Course time conflict'
    UNKNOWN = "Unknown error"
    MSG_404 = 'This message id doesn\'t exist'

    HOT_EDIT = "Hot edit is not allowed"
    GT_ONE = 'Addition number greater than one'
    OVERLAP = 'Phase time overlap'
    OUTDATED = "This time point has passed"


class ELE_TYPE:
    NONE = 0
    ELECTED = 1
    PENDING = 2
    NEW_ELECTED = 3
    NEW_FAILED = 4


class OP_TYPE:
    ELECT = 0
    EDIT_WP = 1
    QUIT_PEDING = 2
    DROP = 3


class COURSE_TYPE:
    MAJOR = 0
    POLITICS = 3
    GYM = 4
    ENGLISH = 5
    GENERAL = 6
