from asterisk_ng.plugins.telephony.ami_manager import Event
from asterisk_ng.plugins.telephony.ami_manager import IAmiEventHandler

from asterisk_ng.system.logger import ILogger

from ...core import Channel
from ...core import IReflector


__all__ = [
    "NewCallerIdEventHandler",
]


class NewCallerIdEventHandler(IAmiEventHandler):

    __slots__ = (
        "__reflector",
        "__logger",
    )

    def __init__(
        self,
        reflector: IReflector,
        logger: ILogger,
    ) -> None:
        self.__reflector = reflector
        self.__logger = logger

    async def __call__(self, event: Event) -> None:

        channel_name = event["Channel"]

        if phone_number := event.get("CallerIDNum"):
            await self.__reflector.attach_phone(channel_name, phone=phone_number)
