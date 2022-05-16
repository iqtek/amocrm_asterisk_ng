from glassio.event_bus import EventBusFactory
from glassio.event_bus import IEventBus
from glassio.event_bus import InitializableEventBus
from glassio.event_bus import StandardEventDispatcher
from glassio.logger import ILogger
from glassio.message_bus import InitializableMessageBus
from glassio.message_bus import MemoryMessageBusFactory

from amocrm_asterisk_ng.infrastructure import ioc

from .events import BaseEvent
from .events import EventSerializer


__all__ = [
    "event_bus_startup",
]


def event_bus_startup() -> None:
    logger = ioc.get_instance(ILogger)

    event_serializer = EventSerializer()
    message_bus_factory = MemoryMessageBusFactory(logger=logger)
    message_bus = message_bus_factory.get_instance()
    event_dispatcher = StandardEventDispatcher(default=message_bus)

    event_bus_factory: EventBusFactory[BaseEvent] = EventBusFactory(
        event_serializer=event_serializer,
        logger=logger,
        event_dispatcher=event_dispatcher,
    )

    event_bus = event_bus_factory.get_instance(
        {"number_of_consumers": {message_bus: 1}}
    )

    ioc.set_instance(InitializableEventBus, event_bus)
    ioc.set_instance(IEventBus, event_bus)
    ioc.set_instance(InitializableMessageBus, message_bus)

    infrastructure_components = ioc.get("infrastructure_components")
    infrastructure_components.append(message_bus)
    infrastructure_components.append(event_bus)
