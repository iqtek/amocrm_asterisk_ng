from asterisk_ng.plugins.telephony.ami_manager import Event
from asterisk_ng.plugins.telephony.ami_manager import IAmiEventHandler

from asterisk_ng.system.logger import ILogger

from ...core import Channel
from ...core import IReflector


__all__ = [
    "NewChannelEventHandler",
]


class NewChannelEventHandler(IAmiEventHandler):

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
        unique_id = event["Uniqueid"]
        linked_id = event["Linkedid"]
        channel_state_desc = event["ChannelStateDesc"]

        channel = Channel(
            name=channel_name,
            unique_id=unique_id,
            linked_id=linked_id,
            state=channel_state_desc.capitalize(),
        )

        await self.__reflector.add_channel(channel)

        if phone := event.get("CallerIDNum", None):
            await self.__reflector.attach_phone(channel_name, phone)
