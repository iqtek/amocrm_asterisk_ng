from .IAmiEventHandler import IAmiEventHandler

from .packets import Action
from .packets import Response


__all__ = ["IAmiManager"]


class IAmiManager:

    __slots__ = ()

    async def send_action(self, action: Action) -> None:
        raise NotImplementedError()

    def attach_event_handler(self, event_pattern: str, event_handler: IAmiEventHandler) -> None:
        raise NotImplementedError()
