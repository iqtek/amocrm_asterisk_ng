from abc import ABC
from collections import defaultdict

from typing import MutableMapping
from typing import Set
from typing import Type
from typing import TypeVar
from typing import Union

from amocrm_asterisk_ng.infrastructure import ILogger
from ..core import (
    HandlerNotAttachedFoundException,
    HandlerAlreadyAttachedException,
    IEvent,
    IEventBus,
    IEventHandler,
)


__all__ = [
    "AbstractEventBus",
]


T = TypeVar('T', bound=IEvent)
H = TypeVar('H', bound=IEventHandler)


class AbstractEventBus(IEventBus, ABC):

    __slots__ = (
        "__handlers",
        "__logger",
    )

    def __init__(self, logger: ILogger) -> None:
        self.__handlers:  MutableMapping[Type[T], Set[IEventHandler[T]]] = defaultdict(set)
        self.__logger = logger

    def _get_event_type(
        self,
        handler: Union[IEventHandler, Type[IEventHandler]]
    ) -> Type[IEvent]:
        try:
            return handler.__call__.__annotations__["event"]
        except KeyError:
            raise AttributeError("Handler missing event annotation.")

    def __get_handler(self, handler: Type[H]) -> H:
        event_type = self._get_event_type(handler)
        try:
            result = filter(
                lambda x: type(x) == handler,
                self.__handlers[event_type]
            )
            return list(result)[0]
        except IndexError:
            raise HandlerNotAttachedFoundException(handler)

    async def attach_event_handler(self, event_handler: IEventHandler) -> None:
        try:
            self.__get_handler(type(event_handler))
        except HandlerNotAttachedFoundException:
            event_type = self._get_event_type(event_handler)
            self.__handlers[event_type].add(event_handler)
        else:
            raise HandlerAlreadyAttachedException(type(event_handler))

    async def detach_event_handler(self, event_handler: Type[IEventHandler]) -> None:
        event_type = self._get_event_type(event_handler)
        handler = self.__get_handler(event_handler)
        handlers = self.__handlers[event_type]
        handlers.remove(handler)

    async def _publish(self, event: IEvent) -> None:
        try:
            handlers = self.__handlers[type(event)]
        except KeyError:
            self.__logger.debug(
                f"EventBus: "
                f"not found handler for event: {event!r}."
            )
            return

        for handler in handlers:
            self.__logger.debug(f"EventBus: handler: '{handler}' called.")
            try:
                await handler(event)
            except Exception as e:
                self.__logger.warning(
                    f"EventBus: error calling handler '{handler}' "
                    f"for event: {event}. {e}"
                )
                self.__logger.exception(e)
                raise e
