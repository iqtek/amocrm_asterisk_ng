from typing import Type

from .IAmiEventHandler import IAmiEventHandler
from .packets import Action
from .packets import Response


__all__ = [
    "IAmiManager",
]


class IAmiManager:

    __slots__ = ()

    def connect(self) -> None:
        raise NotImplementedError()

    def disconnect(self) -> None:
        raise NotImplementedError()

    async def send_action(self, action: Action) -> Response:
        raise NotImplementedError()

    def attach_event_handler(self, event_handler: IAmiEventHandler) -> None:
        raise NotImplementedError()

    def detach_event_handler(self, handler_type: Type[IAmiEventHandler]) -> None:
        raise NotImplementedError()
