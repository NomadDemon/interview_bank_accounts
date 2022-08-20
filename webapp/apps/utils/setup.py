from os import getenv
from typing import Any


def env(key: str, fallback: Any = None):
    value = getenv(key)

    # bool
    if value == "true":
        return True

    if value == "false":
        return False

    # list
    if value and value.startswith("(") and value.endswith(")"):
        return value[1:-1].split("|")

    # fallback
    if not value:
        return fallback

    return value
