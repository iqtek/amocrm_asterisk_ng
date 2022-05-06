from typing import Type

from .IEvent import IEvent
from .IEventHandler import IEventHandler


__all__ = [
    "IEventBus",
]


class IEventBus:

    __slots__ = ()

    async def attach_event_handler(
        self,
        event_handler: IEventHandler
    ) -> None:
        """
        Attach an event handler.

        The event type is described in the handler annotation.
        :raise AttributeError: If handler missing event annotation.
        :raise HandlerAlreadyAttachedException: If handler already attached.
        """
        raise NotImplementedError()

    async def detach_event_handler(
        self,
        event_handler: Type[IEventHandler]
    ) -> None:
        """
        Detach an event handler.

        :raise AttributeError: If handler missing event annotation.
        :raise HandlerAlreadyAttachedException: If handler is not attached.
        """
        raise NotImplementedError()

    async def publish(self, event: IEvent) -> None:
        """Ordered to call all handlers for the event."""
        raise NotImplementedError()
