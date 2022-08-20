from .base import *  # noqa

print("# dev config")


# =====================================
# Site constants
# =====================================
SITE_STATUS = ""


# =====================================
# Configuration
# =====================================
ALLOWED_HOSTS = ["*"]
DEBUG = True


# =====================================
# Celery
# =====================================


# =====================================
# Email
# =====================================
EMAIL_FAIL_SILENTLY = False


# =====================================
# Templates
# =====================================
TEMPLATES[0]["OPTIONS"]["debug"] = DEBUG
