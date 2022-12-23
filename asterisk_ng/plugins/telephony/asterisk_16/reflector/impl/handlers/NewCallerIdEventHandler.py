import re

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
        "__internal_number_pattern",
        "__reflector",
        "__logger",
    )

    def __init__(
        self,
        internal_number_pattern: str,
        reflector: IReflector,
        logger: ILogger,
    ) -> None:
        self.__internal_number_pattern = internal_number_pattern
        self.__reflector = reflector
        self.__logger = logger

    async def __call__(self, event: Event) -> None:

        channel_name = event["Channel"]

        if phone_number := event.get("CallerIDNum"):
            pattern=f"^{self.__internal_number_pattern}$"
            result = re.search(pattern, phone_number)

            if result is not None:
                await self.__reflector.attach_phone(channel_name, phone=phone_number)
                return
