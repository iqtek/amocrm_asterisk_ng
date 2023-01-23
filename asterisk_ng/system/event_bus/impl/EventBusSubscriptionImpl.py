from typing import Type

from ..core import BaseEvent
from ..core import IEventBusSubscription
from ..core import IEventHandler


__all__ = [
    "EventBusSubscriptionImpl",
]


class EventBusSubscriptionImpl(IEventBusSubscription):

    __slots__ = (
        "__event_type",
        "__event_handler",
    )

    def __init__(
        self,
        event_type: Type[BaseEvent],
        event_handler: IEventHandler
    ) -> None:
        self.__event_type = event_type
        self.__event_handler = event_handler

    @property
    def event_type(self) -> Type[BaseEvent]:
        return self.__event_type

    @property
    def event_handler(self) -> IEventHandler:
        return self.__event_handler
