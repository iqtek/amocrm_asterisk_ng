from asyncio import create_task, sleep
from datetime import datetime

from asterisk_ng.interfaces import RingingTelephonyEvent
from asterisk_ng.plugins.telephony.ami_manager import Event
from asterisk_ng.plugins.telephony.ami_manager import IAmiEventHandler
from asterisk_ng.system.event_bus import IEventBus
from asterisk_ng.system.logger import ILogger

from ...core import IReflector


__all__ = ["DialStateEventHandler"]


class DialStateEventHandler(IAmiEventHandler):

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

        if event["DialStatus"] != "RINGING":
            return

        if "Channel" not in event.keys():
            return

        channel = event["Channel"]
        dest_channel = event["DestChannel"]

        async def task() -> None:
            await sleep(2.0)

            try:
                caller_phone_number = await self.__reflector.get_phone(channel)
                called_phone_number = await self.__reflector.get_phone(dest_channel)
            except KeyError:
                return

            ringing_event = RingingTelephonyEvent(
                caller_phone_number=caller_phone_number,
                called_phone_number=called_phone_number,
                created_at=datetime.now()
            )

            await self.__event_bus.publish(ringing_event)

        create_task(task())
