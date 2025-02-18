from os import environ as env

from .dev import * # noqa

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = dict(
    default=dict(
        ENGINE="django.db.backends.postgresql",
        NAME=env.get("DB_NAME", "postgres"),
        HOST=env.get("DB_HOST", "db"),
        PORT=env.get("DB_PORT", "5432"),
        USER=env.get("DB_USER", "postgres"),
        PASSWORD=env.get("DB_PASSWORD", "nestino"),
        OPTIONS=dict(
            connect_timeout=3,
        ),
    )
)


try:
    from .local import *
except ImportError:
    pass
