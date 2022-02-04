from asterisk_amocrm.infrastructure.logger import ILogger
from .DispatcherImpl import DispatcherImpl
from ..core import IDispatcher

__all__ = [
    "dispatcher_startup",
]


def dispatcher_startup(logger: ILogger) -> IDispatcher:
    dispatcher = DispatcherImpl(logger=logger)
    return dispatcher

