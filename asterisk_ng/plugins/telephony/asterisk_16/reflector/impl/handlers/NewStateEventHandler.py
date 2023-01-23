from asterisk_ng.plugins.telephony.ami_manager import Event
from asterisk_ng.plugins.telephony.ami_manager import IAmiEventHandler
from datetime import datetime
from asterisk_ng.interfaces import CallCreatedTelephonyEvent

from asterisk_ng.system.event_bus import IEventBus
from asterisk_ng.system.logger import ILogger

from ...core import Channel
from ...core import IReflector


__all__ = [
    "NewStateEventHandler",
]


class NewStateEventHandler(IAmiEventHandler):

    __slots__ = (
        "__reflector",
        "__event_bus",
        "__logger",
    )

    def __init__(
        self,
        reflector: IReflector,
        event_bus: IEventBus,
        logger: ILogger,
    ) -> None:
        self.__reflector = reflector
        self.__event_bus = event_bus
        self.__logger = logger

    async def __call__(self, event: Event) -> None:

        channel_name = event["Channel"]
        new_state = event["ChannelStateDesc"]
        linked_id = event["Linkedid"]

        if new_state != "Up":
            return

        try:
            phone = await self.__reflector.get_phone(channel_name)
        except KeyError:
            return

        await self.__reflector.add_to_call(
            linked_id=linked_id,
            phone=phone,
        )

        phones = await self.__reflector.get_call_phones(linked_id)
        channel = await self.__reflector.get_channel_by_phone(phones[0])

        if len(phones) != 2:
            return

        if channel.linked_id == channel.unique_id:
            caller_phone_number, called_phone_number = phones
        else:
            called_phone_number, caller_phone_number = phones

        call_created_telephony_event = CallCreatedTelephonyEvent(
            unique_id=linked_id,
            caller_phone_number=caller_phone_number,
            called_phone_number=called_phone_number,
            created_at=datetime.now()
        )

        await self.__event_bus.publish(call_created_telephony_event)
