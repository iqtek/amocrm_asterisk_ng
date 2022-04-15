from amocrm_asterisk_ng.infrastructure import ioc
from amocrm_asterisk_ng.version import APP_VERSION

from .GetCurrentAppVersionFunction import GetCurrentAppVersionFunction
from ..core import IGetCurrentAppVersionFunction
from ..core import Version


__all__ = [
    "get_current_version_func_startup",
    "get_current_version_func",
]


def get_current_version_func(
    version: str,
) -> IGetCurrentAppVersionFunction:
    numbers = version.split('.')
    current_version = Version(*numbers)
    return GetCurrentAppVersionFunction(current_version)


def get_current_version_func_startup() -> None:
    str_version = APP_VERSION

    instance = get_current_version_func(str_version)

    ioc.set_instance(
        key=IGetCurrentAppVersionFunction,
        instance=instance,
    )
