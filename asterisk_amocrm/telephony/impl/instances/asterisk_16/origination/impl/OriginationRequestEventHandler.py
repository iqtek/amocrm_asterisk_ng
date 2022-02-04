from asterisk_amocrm.domains import OriginationRequestEvent
from asterisk_amocrm.infrastructure import IDispatcher, IEventHandler
from ..core import OriginationCallCommand


__all__ = [
    "OriginationRequestEventHandler",
]


class OriginationRequestEventHandler(IEventHandler):

    def __init__(self, dispatcher: IDispatcher) -> None:
        self.__dispatcher = dispatcher

    async def __call__(self, event: OriginationRequestEvent) -> None:
        command = OriginationCallCommand(**event.dict())
        await self.__dispatcher.on_command(command)
