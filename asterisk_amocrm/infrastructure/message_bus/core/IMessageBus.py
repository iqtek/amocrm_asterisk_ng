from typing import Optional

from .IConsumer import IConsumer
from .Message import Message
from .Properties import Properties


__all__ = [
    "IMessageBus",
]


class IMessageBus:

    __slots__ = ()

    async def publish(
        self,
        message: Message,
        properties: Optional[Properties] = None
    ) -> None:
        """
        Publish message.

        The added consumers will be called.
        """
        raise NotImplementedError()

    async def add_consumer(self, consumer: IConsumer) -> None:
        """Add a consumer."""
        raise NotImplementedError()
