from asterisk_ng.plugins.telephony.ami_manager import Event
from asterisk_ng.plugins.telephony.ami_manager import IAmiEventHandler

from asterisk_ng.system.event_bus import IEventBus
from asterisk_ng.system.logger import ILogger

from ...core import Channel
from ...core import IReflector


__all__ = [
    "BridgeLeaveEventHandler",
]


class BridgeLeaveEventHandler(IAmiEventHandler):

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

        await self.__reflector.bridge_leave_channel(
            bridge_unique_id=bridge_unique_id,
            channel_name=channel_name,
        )
