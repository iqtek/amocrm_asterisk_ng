from typing import Generic
from typing import TypeVar

from .BaseEvent import BaseEvent


__all__ = ["IEventHandler"]


E = TypeVar('E')


class IEventHandler(Generic[E]):

    __slots__ = ()

    async def __call__(self, event: E) -> None:
        raise NotImplementedError()
