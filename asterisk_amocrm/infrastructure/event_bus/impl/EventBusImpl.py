from collections import defaultdict
from typing import (
    Generic,
    TypeVar,
    Union,
    Type,
    Dict,
    Set,
)

from ..core import (
    IEvent,
    IEventBus,
    IEventHandler,
    HandlerAlreadyAttachedException,
    HandlerNotAttachedFoundException,
)
from ...logger import ILogger


__all__ = [
    "EventBusImpl",
]


T = TypeVar("T", bound=IEventHandler)


class EventBusImpl(IEventBus, Generic[T]):

    __slots__ = (
        "__event_handlers",
        "_logger"
    )

    def __init__(
        self,
        logger: ILogger,
    ) -> None:
        self.__event_handlers:  Dict[Type[IEvent], Set[IEventHandler]] = defaultdict(set)
        self.__logger = logger

    def __get_event_type(
        self,
        handler: Union[IEventHandler, Type[IEventHandler]]
    ) -> Type[IEvent]:
        try:
            return handler.__call__.__annotations__["event"]
        except KeyError:
            raise AttributeError("Handler missing event annotation.")

    def __get_handler(self, handler: Type[T]) -> T:
        event_type = self.__get_event_type(handler)
        try:
            return list(filter(lambda x: type(x), self.__event_handlers[event_type]))[0]
        except IndexError:
            raise HandlerNotAttachedFoundException(handler)

    async def attach_event_handler(self, event_handler: IEventHandler) -> None:
        try:
            self.__get_handler(type(event_handler))
        except HandlerNotAttachedFoundException:
            event_type = self.__get_event_type(event_handler)
            self.__event_handlers[event_type].add(event_handler)
            self.__logger.debug(
                "EventBus: "
                f"attach handler={event_handler} "
                f"for event={event_type}."
            )
        else:
            raise HandlerAlreadyAttachedException(type(event_handler))

    async def detach_event_handler(self, event_handler: Type[IEventHandler]):
        event_type = self.__get_event_type(event_handler)
        handler = self.__get_handler(event_handler)
        handlers = self.__event_handlers[event_type]
        handlers.remove(handler)
        self.__logger.debug(
            "EventBus: "
            f"detach handler: {event_handler} for "
            f"event: {event_type}."
        )

    async def on_event(self, event: IEvent) -> None:
        self.__logger.debug(
            "EventBus: "
            f"caught event={event!r}."
        )
        try:
            handlers = self.__event_handlers[type(event)]
        except KeyError:
            self.__logger.warning(
                f"EventBus: not found eventHandler for event={event}."
            )
            return

        for handler in handlers:
            self.__logger.debug(f"EventBus: handler={handler} called.")
            try:
                await handler(event)
            except Exception as e:
                self.__logger.warning(
                    f"EventBus: error calling handler={handler} "
                    f"for event: {event}. exc={e!r}"
                )
