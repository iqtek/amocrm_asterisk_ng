from typing import Any
from typing import Mapping

from .Message import Message
from .Properties import Properties


__all__ = [
    "IConsumer",
]


class IConsumer:

    async def __call__(
        self,
        message: Message,
        properties: Properties,
    ) -> None:
        """
        Consume a message.

        If the consumer throws an exception,
        the message will not be removed from the queue.

        :param message: Consumed message.
        :param properties: Message properties.
        :return: None
        """
        raise NotImplementedError()
