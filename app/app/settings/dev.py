import os

from .base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-tk5(kqi@02d^jhet^v@6etar4dmb$20sn^vs1xv!fmp=86+-pj"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]


INSTALLED_APPS += [
    "wagtail.contrib.styleguide",
]


TEMPLATES[0]["OPTIONS"]["debug"] = DEBUG


# Email settings

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# Authentication and security

# Set these options to True to test security functionalies locally.
AXES_ENABLED = False


# Static files (CSS, JavaScript, Images, fonts)

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, "static"),
]

# Django vite
DJANGO_VITE = {
    "default": {
        "dev_mode": True,
        "static_url_prefix": FRONTEND_ASSETS_URL_PREFIX,
    }
}


# Wagtail

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = "http://localhost:8000"

WAGTAIL_ENABLE_UPDATE_CHECK = True


# API

WAGTAILAPI_DEFAULT_RENDERER_CLASSES = [
    "rest_framework.renderers.JSONRenderer",
    "rest_framework.renderers.BrowsableAPIRenderer",
]


try:
    from .local import *
except ImportError:
    pass
