from typing import Callable

from asterisk_ng.plugins.telephony.ami_manager import Event
from asterisk_ng.plugins.telephony.ami_manager import IAmiEventHandler

from asterisk_ng.system.logger import ILogger

from ...core import IReflector


__all__ = [
    "NewCallerIdEventHandler",
]


class NewCallerIdEventHandler(IAmiEventHandler):

    __slots__ = (
        "__is_physical_channel",
        "__reflector",
        "__logger",
    )

    def __init__(
        self,
        is_physical_channel: Callable[[str], bool],
        reflector: IReflector,
        logger: ILogger,
    ) -> None:
        self.__is_physical_channel = is_physical_channel
        self.__reflector = reflector
        self.__logger = logger

    async def __call__(self, event: Event) -> None:

        channel_name = event["Channel"]
        phone_number = event.get("CallerIDNum", None)

        if not self.__is_physical_channel(channel_name):
            return

        if phone_number is None:
            return

        channel = await self.__reflector.get_channel_by_name(event["Channel"])

        if channel.phone is None:
            await self.__reflector.update_channel_phone(channel_name, phone=phone_number)
