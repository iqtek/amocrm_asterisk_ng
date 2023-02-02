from typing import Callable
from datetime import datetime

from asterisk_ng.interfaces import CallCreatedTelephonyEvent, RingingTelephonyEvent, CallCompletedTelephonyEvent

from asterisk_ng.plugins.telephony.ami_manager import Event
from asterisk_ng.plugins.telephony.ami_manager import IAmiEventHandler

from asterisk_ng.system.event_bus import IEventBus
from asterisk_ng.system.logger import ILogger

from ...core import IReflector


__all__ = [
    "NewStateEventHandler",
]


class NewStateEventHandler(IAmiEventHandler):

    __slots__ = (
        "__is_physical_channel",
        "__reflector",
        "__event_bus",
        "__logger",
    )

    def __init__(
        self,
        is_physical_channel: Callable[[str], bool],
        reflector: IReflector,
        event_bus: IEventBus,
        logger: ILogger,
    ) -> None:
        self.__is_physical_channel = is_physical_channel
        self.__reflector = reflector
        self.__event_bus = event_bus
        self.__logger = logger

    async def __call__(self, event: Event) -> None:

        channel_name = event["Channel"]
        new_state = event["ChannelStateDesc"]
        linked_id = event["Linkedid"]

        if not self.__is_physical_channel(channel_name):
            return

        channel = await self.__reflector.get_channel_by_name(channel_name)
        root_channel = await self.__reflector.get_channel_by_unique_id(linked_id)

        if channel.unique_id == root_channel.unique_id:
            return

        if new_state == "Ringing":
            await self.__reflector.update_channel_state(channel_name, new_state)
            ringing_telephony_event = RingingTelephonyEvent(
                caller_phone_number=root_channel.phone,
                called_phone_number=channel.phone,
                created_at=datetime.now(),
            )

            await self.__event_bus.publish(ringing_telephony_event)
            return

        if new_state == "Up":
            await self.__reflector.update_channel_state(channel_name, new_state)
            call_created_telephony_event = CallCreatedTelephonyEvent(
                unique_id=linked_id,
                caller_phone_number=root_channel.phone,
                called_phone_number=channel.phone,
                created_at=datetime.now()
            )

            await self.__event_bus.publish(call_created_telephony_event)
            return
