from typing import Any
from typing import Mapping

from asterisk_amocrm.infrastructure import ioc
from .get_logger import get_logger
from ..core import ILogger


__all__ = [
    "logger_startup",
]


def logger_startup(
    settings: Mapping[str, Any],
) -> None:
    instance = get_logger(settings=settings)

    ioc.set_instance(
        key=ILogger,
        instance=instance,
    )
