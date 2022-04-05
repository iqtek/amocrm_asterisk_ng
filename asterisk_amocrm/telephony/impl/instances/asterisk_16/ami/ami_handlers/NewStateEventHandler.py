from asterisk_amocrm.domains import RingingEvent
from asterisk_amocrm.infrastructure import IEventBus
from asterisk_amocrm.infrastructure import ILogger

from ..ami_store import IAmiStore
from ......core.ami_manager import Event
from ......core.ami_manager import IAmiEventHandler


__all__ = [
    "NewStateEventHandler",
]


class NewStateEventHandler(IAmiEventHandler):

    __slots__ = (
        "__event_bus",
        "__ami_store",
        "__logger",
    )

    def __init__(
        self,
        event_bus: IEventBus,
        ami_store: IAmiStore,
        logger: ILogger,
    ) -> None:
        self.__event_bus = event_bus
        self.__ami_store = ami_store
        self.__logger = logger

    @classmethod
    def event_pattern(cls) -> str:
        return "Newstate"

    async def __call__(self, event: Event) -> None:

        if event["ChannelStateDesc"] != "Ringing":
            return

        called_unique_id = event["Uniqueid"]

        caller_unique_id = await self.__ami_store.get_unique_id_by_dialbegin(
            unique_id=called_unique_id
        )
        caller_channel = await self.__ami_store.get_channel_by_unique_id(
            caller_unique_id
        )
        called_channel = await self.__ami_store.get_channel_by_unique_id(
            called_unique_id
        )
        caller_phone_number = await self.__ami_store.get_phone_by_channel(
            caller_channel
        )
        called_phone_number = await self.__ami_store.get_phone_by_channel(
            called_channel
        )

        ringing_event = RingingEvent(
            caller_phone_number=caller_phone_number,
            called_phone_number=called_phone_number,
        )

        await self.__event_bus.publish(ringing_event)
