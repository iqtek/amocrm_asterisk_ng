from typing import Any
from typing import Mapping
from typing import Tuple

from time import time

from ....core import Message
from ....core import Properties


__all__ = [
    "MessageWrapper",
]


class MessageWrapper:

    __slots__ = (
        "__properties",
        "__message",
        "__priority"
    )

    def __init__(
        self,
        properties: Properties,
        message: Message,
    ) -> None:
        if properties.expiration is not None and \
                properties.timestamp is None:
            properties.timestamp = time()

        # Priority inversion for asyncio queue.
        priority = properties.priority or 0
        priority = 10 - priority

        self.__properties = properties
        self.__message = message
        self.__priority = priority

    @property
    def priority(self) -> int:
        return self.__priority

    def unwrap(
        self,
        time_now: float,
    ) -> Tuple[Properties, Message]:

        if self.__properties.expiration is None:
            return self.__properties, self.__message

        if self.__properties.timestamp + \
                self.__properties.expiration >= time_now:
            return self.__properties, self.__message

        raise TimeoutError("Message ttl expired.")

    def __eq__(self, other: 'MessageWrapper'):
        return self.priority == other.priority

    def __lt__(self, other: 'MessageWrapper'):
        return self.priority < other.priority

    def __gt__(self, other: 'MessageWrapper'):
        return self.priority > other.priority

    def __repr__(self) -> str:
        return f"properties: {self.__properties}, " \
               f"message: {self.__message}"
