from datetime import datetime
from typing import Callable

from asterisk_ng.interfaces import CallCompletedTelephonyEvent, CallStatus

from asterisk_ng.plugins.telephony.ami_manager import Event
from asterisk_ng.plugins.telephony.ami_manager import IAmiEventHandler

from asterisk_ng.system.event_bus import IEventBus
from asterisk_ng.system.logger import ILogger

from ...core import IReflector


__all__ = [
    "HangupEventHandler",
]


class HangupEventHandler(IAmiEventHandler):

    __slots__ = (
        "__is_physical_channel",
        "__event_bus",
        "__reflector",
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
        linked_id = event["Linkedid"]

        if not self.__is_physical_channel(channel_name):
            return

        root_channel = await self.__reflector.get_channel_by_name(channel_name)

        if root_channel.unique_id != root_channel.linked_id:
            return  # not root channel

        call = await self.__reflector.get_call(root_channel.linked_id)

        for channel_unique_id in call.channels_unique_ids:
            channel = await self.__reflector.get_channel_by_unique_id(channel_unique_id)

            if channel.state == "up":
                call_completed_telephony_event = CallCompletedTelephonyEvent(
                    unique_id=linked_id,
                    disposition=CallStatus.ANSWERED,
                    caller_phone_number=root_channel.phone,
                    called_phone_number=channel.phone,
                    created_at=datetime.now()
                )
                break
        else:
            if len(call.channels_unique_ids) == 1:
                called_phone_number = (await self.__reflector.get_channel_by_unique_id(call.channels_unique_ids[0])).phone
            else:
                called_phone_number = None

            call_completed_telephony_event = CallCompletedTelephonyEvent(
                unique_id=linked_id,
                disposition=CallStatus.NO_ANSWER,
                caller_phone_number=root_channel.phone,
                called_phone_number=called_phone_number,
                created_at=datetime.now()
            )

        for channel_unique_id in call.channels_unique_ids:
            await self.__reflector.delete_channel_from_call(root_channel.linked_id, channel_unique_id)

        await self.__reflector.save_call_completed_event(linked_id, call_completed_telephony_event)
        await self.__event_bus.publish(call_completed_telephony_event)
        await self.__reflector.delete_call(root_channel.linked_id)
