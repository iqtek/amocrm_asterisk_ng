from asterisk_amocrm.domains import OriginationRequestEvent
from asterisk_amocrm.infrastructure import IDispatcher, IEventHandler
from ..core import IOriginationCallCommand


__all__ = [
    "OriginationRequestEventHandler",
]


class OriginationRequestEventHandler(IEventHandler):

    __slots__ = (
        "__origination_call_command"
    )

    def __init__(
        self,
        origination_call_command: IOriginationCallCommand
    ) -> None:
        self.__origination_call_command = origination_call_command

    async def __call__(self, event: OriginationRequestEvent) -> None:
        await self.__origination_call_command(**event.dict())
