"""
Django settings for wagtailstarter project.

Generated by 'django-admin startproject' using Django 5.1.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from datetime import timedelta


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)


VERSION = "0.1.0"


# General base settings
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    "users",
    "home",
    "search",
    "nest",
    "flexiblepages",
    "menus",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.contrib.routable_page",
    "wagtail.contrib.search_promotions",
    "wagtail.contrib.settings",
    "wagtail.api.v2",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "modelcluster",
    "taggit",
    "rest_framework",
    "django_vite",
    "axes",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # "django.contrib.sites",
    # "django.contrib.sitemaps",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "axes.middleware.AxesMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "app.context.globals",
            ],
        },
    },
]

WSGI_APPLICATION = "app.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# Fixes warning with third party modules
# "Auto-created primary key used when not defining a primary key type"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Authentication and security

AUTH_USER_MODEL = "users.User"

AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesBackend",
    "django.contrib.auth.backends.ModelBackend",
]

# django-axes
# https://django-axes.readthedocs.io/en/latest/4_configuration.html#configuring-project-settings
AXES_FAILURE_LIMIT = 5  # Number of allowed failed attempts
AXES_COOLOFF_TIME = timedelta(minutes=5)  # Lockout cooloff
AXES_LOCKOUT_PARAMETERS = ["username"]
AXES_LOCKOUT_TEMPLATE = "wagtailadmin/lockout.html"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-gb"

TIME_ZONE = "Europe/London"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static and media files (CSS, JavaScript, images, videos, etc.)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

FRONTEND_ASSETS_URL_PREFIX = "frontend"

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, "static"),
    (
        FRONTEND_ASSETS_URL_PREFIX,
        os.path.join(BASE_DIR, "assets"),
    ),  # Frontend build assets
]

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

# Django Vite
# https://github.com/MrBin99/django-vite?tab=readme-ov-file#configuration
DJANGO_VITE = {
    "default": {
        "dev_mode": False,
        "static_url_prefix": FRONTEND_ASSETS_URL_PREFIX,
    }
}


# Default storage settings, with the staticfiles storage updated.
# See https://docs.djangoproject.com/en/5.1/ref/settings/#std-setting-STORAGES
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    # ManifestStaticFilesStorage is recommended in production, to prevent
    # outdated JavaScript / CSS assets being served from cache
    # (e.g. after a Wagtail upgrade).
    # See https://docs.djangoproject.com/en/5.1/ref/contrib/staticfiles/#manifeststaticfilesstorage
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    },
}

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"


# Wagtail

WAGTAIL_SITE_NAME = "Wagtail App Nest"


# Search
# https://docs.wagtail.org/en/stable/topics/search/backends.html
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    }
}

WAGTAILIMAGES_IMAGE_MODEL = "nest.CustomImage"
WAGTAILDOCS_DOCUMENT_MODEL = "nest.CustomDocument"
WAGTAILDOCS_EXTENSIONS = ["pdf", "doc", "docx", "xls", "xlsx", "csv", "pptx"]

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = "http://example.com"

# Displays the "update Wagtail" message in the CMS dashboard if a new version
# of Wagtail is available.
# Keep it disabled in production
WAGTAIL_ENABLE_UPDATE_CHECK = False


# API

WAGTAILAPI_DEFAULT_RENDERER_CLASSES = [
    "rest_framework.renderers.JSONRenderer",
]
