from typing import Any
from typing import Callable
from typing import Coroutine

from amocrm_asterisk_ng.infrastructure import IConsumer
from amocrm_asterisk_ng.infrastructure import ILogger
from amocrm_asterisk_ng.infrastructure import IMessageBus

from .EventBusConsumer import EventBusConsumer
from ...core import ISerializer
from ......core import IEvent


__all__ = [
    "ConsumerFactory",
]


class ConsumerFactory:

    __slots__ = (
        "__event_to_bytes_serializer",
        "__message_bus",
        "__logger",
    )

    def __init__(
        self,
        event_to_bytes_serializer: ISerializer[IEvent, bytes],
        message_bus: IMessageBus,
        logger: ILogger,
    ) -> None:
        self.__event_to_bytes_serializer = event_to_bytes_serializer
        self.__message_bus = message_bus
        self.__logger = logger

    def get_instance(
        self,
        callback: Callable[[IEvent], Coroutine[Any, Any, None]]
    ) -> IConsumer:

        return EventBusConsumer(
            event_to_bytes_serializer=self.__event_to_bytes_serializer,
            callback=callback,
            message_bus=self.__message_bus,
            logger=self.__logger,
        )
