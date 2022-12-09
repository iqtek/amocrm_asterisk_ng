from asterisk_ng.plugins.telephony.ami_manager import Event
from asterisk_ng.plugins.telephony.ami_manager import IAmiEventHandler

from asterisk_ng.system.event_bus import IEventBus
from asterisk_ng.system.logger import ILogger

from ...core import Channel
from ...core import IReflector


__all__ = [
    "BridgeDestroyEventHandler",
]


class BridgeDestroyEventHandler(IAmiEventHandler):

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
        await self.__reflector.delete_bridge(event["BridgeUniqueid"])
