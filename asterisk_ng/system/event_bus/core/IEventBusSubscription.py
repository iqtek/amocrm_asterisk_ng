from typing import Type

from .BaseEvent import BaseEvent
from .IEventHandler import IEventHandler


__all__ = ["IEventBusSubscription"]


class IEventBusSubscription:

    __slots__ = ()

    @property
    def event_type(self) -> Type[BaseEvent]:
        raise NotImplementedError()

    @property
    def event_handler(self) -> IEventHandler:
        raise NotImplementedError()
