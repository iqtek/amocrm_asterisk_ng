from typing import Any
from typing import Callable
from typing import Coroutine

from amocrm_asterisk_ng.infrastructure import IConsumer
from amocrm_asterisk_ng.infrastructure import ILogger
from amocrm_asterisk_ng.infrastructure import IMessageBus
from amocrm_asterisk_ng.infrastructure import Message
from amocrm_asterisk_ng.infrastructure import Properties

from ...core import ISerializer
from ......core import IEvent


__all__ = [
    "EventBusConsumer",
]


class EventBusConsumer(IConsumer):

    __HEADERS_COUNTER_FIELD = "attempts"
    __HEADERS_CONTEXT_FIELD = "context_snapshot"

    __slots__ = (
        "__event_to_bytes_serializer",
        "__message_bus",
        "__callback",
        "__logger",
    )

    def __init__(
        self,
        event_to_bytes_serializer: ISerializer[IEvent, bytes],
        message_bus: IMessageBus,
        callback: Callable[[IEvent], Coroutine[Any, Any, None]],
        logger: ILogger,
    ) -> None:
        self.__event_to_bytes_serializer = event_to_bytes_serializer
        self.__message_bus = message_bus
        self.__callback = callback
        self.__logger = logger

    async def __call__(self, message: Message, properties: Properties) -> None:

        try:
            event = self.__event_to_bytes_serializer.deserialize(message)
        except Exception as e:
            self.__logger.error(
                "EventBusConsumer: "
                "Unable to deserialize message to event: "
                f"`{message}`. {e}. "
                f"The message is considered consumed."
            )
            return

        try:
            await self.__callback(event)
        except Exception as e:
            self.__logger.error(
                "EventBusConsumer: "
                "Error publishing event. "
                f"event: `{event}`."
            )
            self.__logger.exception(e)
        else:
            return
