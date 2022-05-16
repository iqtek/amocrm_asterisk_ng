from logging import config
from logging import getLogger
from logging import Logger
from typing import Any
from typing import Mapping

from amocrm_asterisk_ng.infrastructure import ioc


__all__ = [
    "logger_startup",
]


def logger_startup(settings: Mapping[str, Any]) -> None:

    if len(settings.keys()) != 0:
        config.dictConfig(dict(settings))

    logger = getLogger("root")
    ioc.set_instance(Logger, logger)
