from asterisk_amocrm.infrastructure.logger import ILogger
from .EventBusImpl import EventBusImpl
from ..core import IEventBus

__all__ = [
    "event_bus_startup",
]


def event_bus_startup(logger: ILogger) -> IEventBus:
    dispatcher = EventBusImpl(logger=logger)
    return dispatcher

