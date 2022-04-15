from amocrm_asterisk_ng.infrastructure.message_bus import IConsumer
from amocrm_asterisk_ng.infrastructure.message_bus import Message
from amocrm_asterisk_ng.infrastructure.message_bus import Properties


__all__ = [
    "SimpleConsumer",
]


class SimpleConsumer(IConsumer):

    __slots__ = (
        "_call_counter",
        "_consumed_message",
        "_consumed_properties",
    )

    def __init__(self) -> None:
        self._call_counter: int = 0
        self._consumed_message: Optional[Message] = None
        self._consumed_properties: Optional[Properties] = None

    @property
    def call_counter(self) -> int:
        return self._call_counter

    @property
    def consumed_message(self) -> Message:
        return self._consumed_message

    @property
    def consumed_properties(self) -> Properties:
        return self._consumed_properties

    async def __call__(self, message: Message, properties: Properties) -> None:
        self._call_counter += 1
        self._consumed_message = message
        self._consumed_properties = properties
