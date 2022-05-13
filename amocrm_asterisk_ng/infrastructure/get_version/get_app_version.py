from amocrm_asterisk_ng.version import APP_VERSION

from .Version import Version


__all__ = [
    "get_app_version",
]


numbers = APP_VERSION.split('.')
current_version = Version(*numbers)


def get_app_version() -> Version:
    return current_version
