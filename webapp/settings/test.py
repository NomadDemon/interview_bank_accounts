from .dev import *  # noqa

print("# testing config")

IS_TEST = True

LANGUAGE_CODE = "en-US"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

CELERY_ALWAYS_EAGER = True

SENTRY_ENABLED = False

LOGGING["loggers"][""]["handlers"] = ["null"]
