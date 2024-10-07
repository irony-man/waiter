"""
Django settings for waiter project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from dotenv import load_dotenv

load_dotenv()


# Standard Library
import os
import sys
from logging.handlers import SysLogHandler
from pathlib import Path

# App Imports
# Build paths inside the project like this: BASE_DIR / 'subdir'.
from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", False) == "True"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

# Application definition

INSTALLED_APPS = [
    # Native
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    # Third Party
    "rest_framework",
    "cloudinary",
    # "phonenumber_field",
    # "django_filters",
    "django_countries",
    # Internal
    "common.apps.CommonConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "common.middleware.PatchRequestMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "common.middleware.TimezoneMiddleware",
]

ROOT_URLCONF = "waiter.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "waiter.wsgi.application"
ASGI_APPLICATION = "waiter.asgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
        "ATOMIC_REQUESTS": True,
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.NumericPasswordValidator"
        ),
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

TIME_FORMAT = "P"

ISO_8601 = "Y-m-d G:i:s"

STRFTIME_DATE_FORMAT = "%B %-d, %Y"

X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

# Warning: %P (capital P) is a platform specific feature and might bomb
# on unsupported platforms like Windows.
STRFTIME_TIME_FORMAT = "%-I:%M %p"
STRFTIME_DATETIME_FORMAT = f"{STRFTIME_DATE_FORMAT} {STRFTIME_TIME_FORMAT}"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR.joinpath("static")
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    # Keep this disabled as this can interfere with django-storages
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

STATICFILES_DIRS = (os.path.join(BASE_DIR, "global_static"),)

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django Vite
DJANGO_VITE_ASSETS_PATH = BASE_DIR / "common" / "static" / "common"
DJANGO_VITE_DEV_MODE = False
DJANGO_VITE_MANIFEST_PATH = (
    BASE_DIR / "common" / "static" / "common" / "manifest.json"
)

# Rest Framework
REST_FRAMEWORK = {
    "DATETIME_FORMAT": STRFTIME_DATETIME_FORMAT,
    "TIME_FORMAT": STRFTIME_TIME_FORMAT,
    "DATE_FORMAT": "iso-8601",
    # ♥♥ strftime and strptime are so lovely ♥♥
    "DATE_INPUT_FORMATS": ["iso-8601", "%b %d, %Y"],
    "TIME_INPUT_FORMATS": ["%I:%M %p", "iso-8601"],  # Ordering sensitive
    "DATETIME_INPUT_FORMATS": ["%Y-%m-%d %I:%M %p", "iso-8601"],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend"
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
        # "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.JSONParser",
    ),
    "DEFAULT_PAGINATION_CLASS": (
        "rest_framework.pagination.LimitOffsetPagination"
    ),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "PAGE_SIZE": 50,
}

# Phone numbers
PHONENUMBER_DB_FORMAT = "E164"
PHONENUMBER_DEFAULT_REGION = "IN"
PHONENUMBER_DEFAULT_FORMAT = "E164"

# Media
MEDIA_URL = "/media/"
MEDIA_ROOT = os.getenv("MEDIA_ROOT")

BASE_URL = os.getenv("BASE_URL")

MEDIAFILES_LOCATION = "media"

REQUESTS_TIMEOUT = 10

LOGIN_URL = reverse_lazy("common:login")
LOGIN_REDIRECT_URL = reverse_lazy("common:dashboard")
LOGOUT_URL = reverse_lazy("common:logout")


import cloudinary

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_NAME"),
    api_key=os.getenv("CLOUDINARY_KEY"),
    api_secret=os.getenv("CLOUDINARY_SECRET"),
)

import cloudinary.api
import cloudinary.uploader

if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
    STATICFILES_STORAGE = (
        "whitenoise.storage.CompressedManifestStaticFilesStorage"
    )
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}
        },
        "formatters": {
            "verbose": {
                "format": "[contactor] %(levelname)s %(asctime)s %(message)s"
            },
        },
        "handlers": {
            # Send all messages to console
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
            },
            # Send info messages to syslog
            "syslog": {
                "level": "INFO",
                "class": "logging.handlers.SysLogHandler",
                "facility": SysLogHandler.LOG_LOCAL2,
                "address": "/dev/log",
                "formatter": "verbose",
            },
            # Warning messages are sent to admin emails
            "mail_admins": {
                "level": "WARNING",
                "filters": ["require_debug_false"],
                "class": "django.utils.log.AdminEmailHandler",
            },
        },
        "loggers": {
            # This is the "catch all" logger
            "django": {
                "handlers": ["console", "syslog", "mail_admins"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    }
