import asyncio

from asterisk_amocrm.infrastructure import ILogger
from ..ami_store import IAmiStore
from ......core.ami_manager import Event
from ......core.ami_manager import IAmiEventHandler


__all__ = [
    "HangupEventHandler",
]


class HangupEventHandler(IAmiEventHandler):

    __DELETE_DELAY: float = 10.0

    __slots__ = (
        "__ami_store",
        "__logger",
    )

    def __init__(
        self,
        ami_store: IAmiStore,
        logger: ILogger
    ) -> None:
        self.__ami_store = ami_store
        self.__logger = logger

    @classmethod
    def event_pattern(cls) -> str:
        return "Hangup"

    async def __call__(self, event: Event) -> None:

        channel = event["Channel"]
        await asyncio.sleep(self.__DELETE_DELAY)
        await self.__ami_store.delete_channel(channel=channel)
