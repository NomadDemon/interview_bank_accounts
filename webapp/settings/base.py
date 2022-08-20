import os

from runenv import load_env

from apps.utils.setup import env

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

load_env(
    env_file=os.path.join(os.path.dirname(BASE_DIR), ".env"),
    prefix=None,
    strip_prefix=False,
    search_parent=1,
)

ENVIRONMENT_TYPE = env("ENV_TYPE")
APP_NAME = env("APP_NAME")

if not any([ENVIRONMENT_TYPE, APP_NAME]):
    print("`.env` not configured")
    raise Exception("`.env` not configured")

ENVIRONMENT_COLORS = {
    "DEV": "gray",
    "STAGING": "purple",
    "PROD": "red",
}
ENVIRONMENT_COLOR = ENVIRONMENT_COLORS[ENVIRONMENT_TYPE]

ADMINS = (("Admin", "hydra@stacja1.pl"),)
MANAGERS = ADMINS
ALLOWED_HOSTS = ["*"]
APPEND_SLASH = True
DEBUG = False
IS_TEST = False

SERVER_NAME = env("SERVER_URL", None)
SECRET_KEY = env("SECRET_KEY", None)
SESSION_COOKIE_DOMAIN = ""
ROOT_URLCONF = "urls_router"
WSGI_APPLICATION = "wsgi.application"


# ===============================================================================
# Celery
# ===============================================================================
CELERY_ENABLED = env("CELERY_ENABLED", False)

# ===============================================================================
# Databases
# ===============================================================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_NAME"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": "db",
        "PORT": 5432,
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ===============================================================================
# CACHE
# ===============================================================================


# ===============================================================================
# Components
# ===============================================================================
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
]

WEBAPP_APPS = [
    "apps.bank_accounts",
]

INSTALLED_APPS = DJANGO_APPS + WEBAPP_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.gzip.GZipMiddleware",
]
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.BCryptPasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.SHA1PasswordHasher",
    "django.contrib.auth.hashers.MD5PasswordHasher",
    "django.contrib.auth.hashers.CryptPasswordHasher",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]


# ===============================================================================
# Internationalization
# ===============================================================================
LANGUAGE_CODE = env("DEFAULT_LANGUAGE", "en-US")
DEFAULT_CHARSET = "utf-8"
TIME_ZONE = "Europe/Warsaw"

USE_I18N = True
USE_TZ = True


# ===============================================================================
# Statics
# ===============================================================================
STATIC_URL = "/static/"
MEDIA_URL = "/site_media/"

STATIC_ROOT = BASE_DIR + "/static_files/"
MEDIA_ROOT = BASE_DIR + "/site_media/"

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


# ===============================================================================
# Email
# ===============================================================================


# ===============================================================================
# Misc.
# ===============================================================================


# =============
# Logger
# =============
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "null": {
            "class": "logging.NullHandler",
        },
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "..", "logs", "django.log"),
            "formatter": "standard",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
            "include_html": True,
        },
    },
    "loggers": {
        "": {
            "handlers": ["file", "console", "mail_admins"],
            "level": "INFO",
        },
    },
}


# ===============================================================================
# Sentry
# ===============================================================================


# ===============================================================================
# REST API
# ===============================================================================
