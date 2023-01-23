from typing import Generic
from typing import Type
from typing import TypeVar

from .BaseEvent import BaseEvent
from .IEventHandler import IEventHandler


__all__ = ["IEventBusSubscription"]


E = TypeVar('E', bound=BaseEvent)


class IEventBusSubscription(Generic[E]):

    __slots__ = ()

    @property
    def event_type(self) -> Type[E]:
        raise NotImplementedError()

    @property
    def event_handler(self) -> IEventHandler[E]:
        raise NotImplementedError()
