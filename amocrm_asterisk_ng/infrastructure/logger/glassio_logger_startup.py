from logging import Logger

from glassio.logger import ILogger
from glassio.logger import InitializableLogger
from glassio.logger import StandardLogger

from amocrm_asterisk_ng.infrastructure import ioc


__all__ = [
    "glassio_logger_startup",
]


def glassio_logger_startup() -> None:
    logger = ioc.get_instance(Logger)
    glassio_logger = StandardLogger(logger)
    ioc.set_instance(InitializableLogger, glassio_logger)
    ioc.set_instance(ILogger, glassio_logger)
