from typing import Any
from typing import Callable
from typing import Coroutine

from asterisk_amocrm.infrastructure import IConsumer
from asterisk_amocrm.infrastructure import ILogger
from asterisk_amocrm.infrastructure import IMessageBus
from asterisk_amocrm.infrastructure import ISetContextVarsFunction

from .EventBusConsumer import EventBusConsumer
from ...core import ISerializer
from ......core import IEvent


__all__ = [
    "ConsumerFactory",
]


class ConsumerFactory:

    __slots__ = (
        "__event_to_bytes_serializer",
        "__set_context_vars_function",
        "__message_bus",
        "__logger",
    )

    def __init__(
        self,
        event_to_bytes_serializer: ISerializer[IEvent, bytes],
        set_context_vars_function: ISetContextVarsFunction,
        message_bus: IMessageBus,
        logger: ILogger,
    ) -> None:
        self.__event_to_bytes_serializer = event_to_bytes_serializer
        self.__set_context_vars_function = set_context_vars_function
        self.__message_bus = message_bus
        self.__logger = logger

    def get_instance(
        self,
        callback: Callable[[IEvent], Coroutine[Any, Any, None]]
    ) -> IConsumer:

        return EventBusConsumer(
            event_to_bytes_serializer=self.__event_to_bytes_serializer,
            set_context_vars_function=self.__set_context_vars_function,
            callback=callback,
            message_bus=self.__message_bus,
            logger=self.__logger,
        )
