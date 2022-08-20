import os

from runenv import load_env

from apps.utils.setup import env

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

dotenv_path = os.path.join(os.path.dirname(BASE_DIR), ".env")

load_env(
    env_file=dotenv_path,
    prefix=None,
    strip_prefix=False,
    search_parent=1,
)

ENVIRONMENT_TYPE = env("ENV_TYPE")

if ENVIRONMENT_TYPE == "DEV":
    from .dev import *  # noqa

elif ENVIRONMENT_TYPE == "STAGING":
    from .staging import *  # noqa

elif ENVIRONMENT_TYPE == "PROD":
    from .prod import *  # noqa

else:
    raise Exception("No .env file or not configured")
