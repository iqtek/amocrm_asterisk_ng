from asterisk_ng.plugins.telephony.ami_manager import Event
from asterisk_ng.plugins.telephony.ami_manager import IAmiEventHandler

from asterisk_ng.interfaces import CallCreatedTelephonyEvent

from asterisk_ng.system.event_bus import IEventBus
from asterisk_ng.system.logger import ILogger

from ...core import Channel
from ...core import IReflector


__all__ = [
    "BridgeEnterEventHandler",
]


class BridgeEnterEventHandler(IAmiEventHandler):

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

        bridge_unique_id = event["BridgeUniqueid"]
        channel_name = event["Channel"]

        await self.__reflector.bridge_enter_channel(
            bridge_unique_id=bridge_unique_id,
            channel_name=channel_name,
        )

        channels = await self.__reflector.get_channels_in_bridge(unique_id=bridge_unique_id)

        if len(channels) != 2:
            return

        phone_1 = await self.__reflector.get_phone(channels[0])
        phone_2 = await self.__reflector.get_phone(channels[1])

        import datetime
        call_created_event = CallCreatedTelephonyEvent(
            unique_id=bridge_unique_id,
            caller_phone_number=phone_2,
            called_phone_number=phone_1,
            created_at=datetime.datetime.now()
        )

        await self.__event_bus.publish(call_created_event)
