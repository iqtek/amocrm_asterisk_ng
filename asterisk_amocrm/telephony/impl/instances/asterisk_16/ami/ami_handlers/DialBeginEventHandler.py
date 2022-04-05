from asterisk_amocrm.infrastructure import ILogger
from ..ami_store import IAmiStore
from ......core.ami_manager import Event
from ......core.ami_manager import IAmiEventHandler


__all__ = [
    "DialBeginEventHandler",
]


class DialBeginEventHandler(IAmiEventHandler):

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
        return "DialBegin"

    async def __call__(self, event: Event) -> None:

        unique_id = event["UniqueID"]
        destination_unique_id = event["DestUniqueID"]

        await self.__ami_store.set_dialbegin(
            unique_id=unique_id,
            dest_unique_id=destination_unique_id
        )
