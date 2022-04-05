from typing import Any
from typing import Callable
from typing import Coroutine

from asterisk_amocrm.infrastructure import ContextSnapshot
from asterisk_amocrm.infrastructure import IConsumer
from asterisk_amocrm.infrastructure import ILogger
from asterisk_amocrm.infrastructure import IMessageBus
from asterisk_amocrm.infrastructure import ISetContextVarsFunction
from asterisk_amocrm.infrastructure import Message
from asterisk_amocrm.infrastructure import Properties

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
        "__set_context_vars_function",
        "__message_bus",
        "__callback",
        "__logger",
    )

    def __init__(
        self,
        event_to_bytes_serializer: ISerializer[IEvent, bytes],
        set_context_vars_function: ISetContextVarsFunction,
        message_bus: IMessageBus,
        callback: Callable[[IEvent], Coroutine[Any, Any, None]],
        logger: ILogger,
    ) -> None:
        self.__event_to_bytes_serializer = event_to_bytes_serializer
        self.__set_context_vars_function = set_context_vars_function
        self.__message_bus = message_bus
        self.__callback = callback
        self.__logger = logger

    async def __call__(self, message: Message, properties: Properties) -> None:
        headers = properties.headers

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

        context_snapshot = headers.get(self.__HEADERS_CONTEXT_FIELD, ContextSnapshot())
        self.__set_context_vars_function(
            snapshot=context_snapshot
        )

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

        attempts = headers.get(self.__HEADERS_COUNTER_FIELD)

        if attempts is None:
            await self.__message_bus.publish(
                message=message,
                properties=Properties(headers=headers)
            )

        if attempts <= 1:
            self.__logger.warning(
                "EventBusConsumer: "
                "The event was removed from the queue "
                "due to exceeding the number of consumption attempts; "
                f"event: `{event}`."
            )
            return

        headers["attempts"] = attempts - 1
        await self.__message_bus.publish(
            message=message,
            properties=Properties(headers=headers)
        )
