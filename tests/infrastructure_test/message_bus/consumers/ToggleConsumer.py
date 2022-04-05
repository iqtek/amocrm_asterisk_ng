from typing import Any
from typing import MutableMapping

from asterisk_amocrm.infrastructure.message_bus import Message
from asterisk_amocrm.infrastructure.message_bus import Properties

from .SimpleConsumer import SimpleConsumer


__all__ = [
    "ToggleConsumer"
]


class ToggleConsumer(SimpleConsumer):

    def __init__(self) -> None:
        super().__init__()

    async def __call__(self, message: Message, properties: Properties) -> None:
        if self._call_counter % 2 == 0:
            self._call_counter += 1
            raise Exception("Message rejected!")

        await super(ToggleConsumer, self).__call__(
            message=message,
            properties=properties,
        )
