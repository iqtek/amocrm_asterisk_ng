from typing import Generic
from typing import TypeVar

from .IEvent import IEvent


__all__ = [
    "IEventHandler",
]


T = TypeVar('T', bound=IEvent)


class IEventHandler(Generic[T]):

    __slots__ = ()

    async def __call__(self, event: T) -> None:
        """
        In the signature of the handler, the `event` argument
        must be specified. Because the binding of the handler
        to the event is done by reading the type annotation
        of this field.
        """
        raise NotImplementedError()
