import logging
from logging import config
from logging import Filter
from logging import getLogger
from logging import StreamHandler
from typing import Any
from typing import Dict

from ..core import ILogger


__all__ = [
    "get_logger",
]


def get_logger(
    settings: Dict[str, Any],
) -> ILogger:

    # if len(settings.keys()) != 0:
    #     config.dictConfig(settings)

    logger = getLogger("root")
    return logger


