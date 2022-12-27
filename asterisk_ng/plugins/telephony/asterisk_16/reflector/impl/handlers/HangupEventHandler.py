from asterisk_ng.plugins.telephony.ami_manager import Event
from asterisk_ng.plugins.telephony.ami_manager import IAmiEventHandler
from datetime import datetime
from asterisk_ng.interfaces import CallCompletedTelephonyEvent
from asterisk_ng.system.event_bus import IEventBus

from asterisk_ng.system.logger import ILogger

from ...core import Channel
from ...core import IReflector


__all__ = [
    "HangupEventHandler",
]


class HangupEventHandler(IAmiEventHandler):

    __slots__ = (
        "__event_bus",
        "__reflector",
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
        linked_id = event["Linkedid"]

        try:
            phones = await self.__reflector.get_call_phones(linked_id)
        except KeyError:
            return

        if len(phones) != 2:
            return

        channel = await self.__reflector.get_channel_by_phone(phones[0])

        await self.__reflector.delete_channel(channel_name)

        if channel.linked_id == channel.unique_id:
            caller_phone_number, called_phone_number = phones
        else:
            called_phone_number, caller_phone_number = phones

        call_completed_telephony_event = CallCompletedTelephonyEvent(
            unique_id=linked_id,
            caller_phone_number=caller_phone_number,
            called_phone_number=called_phone_number,
            created_at=datetime.now()
        )

        await self.__event_bus.publish(call_completed_telephony_event)
