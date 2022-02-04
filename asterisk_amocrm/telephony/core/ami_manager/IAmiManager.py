from .IAmiEventHandler import IAmiEventHandler
from .packets import (
    Action,
    Response,
)


__all__ = [
    "IAmiManager",
]


class IAmiManager:

    def connect(self) -> None:
        raise NotImplementedError()

    def disconnect(self) -> None:
        raise NotImplementedError()

    async def send_action(self, action: Action) -> Response:
        raise NotImplementedError()

    def attach_event_handler(self, event_handler: IAmiEventHandler) -> None:
        raise NotImplementedError()
