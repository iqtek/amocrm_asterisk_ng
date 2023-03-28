from typing import Callable, Optional

from asterisk_ng.plugins.telephony.ami_manager import Event
from asterisk_ng.plugins.telephony.ami_manager import IAmiEventHandler

from ...core import Channel
from ...core import IReflector


__all__ = [
    "NewChannelEventHandler",
]


class NewChannelEventHandler(IAmiEventHandler):

    __slots__ = (
        "__is_physical_channel",
        "__get_phone_by_channel_name",
        "__reflector",
        "__logger",
        "__origination_linked_id",
    )

    def __init__(
        self,
        is_physical_channel: Callable[[str], bool],
        get_phone_by_channel_name: Callable[[str], Optional[str]],
        reflector: IReflector,
    ) -> None:
        self.__is_physical_channel = is_physical_channel
        self.__get_phone_by_channel_name = get_phone_by_channel_name
        self.__reflector = reflector
        self.__origination_linked_id = []

    async def __call__(self, event: Event) -> None:

        channel_name: str = event["Channel"]
        unique_id: str = event["Uniqueid"]
        linked_id: str = event["Linkedid"]
        channel_state_desc: str = event["ChannelStateDesc"]

        if not self.__is_physical_channel(channel_name):
            # The channel is not physical, but root => used origination.
            if unique_id == linked_id:
                self.__origination_linked_id.append(linked_id)
            return

        phone_number = self.__get_phone_by_channel_name(channel_name)

        if phone_number is None:
            phone_number = event.get("CallerIDNum", None)

        if linked_id in self.__origination_linked_id:
            # The first physical channel created after origination will be the root one.
            unique_id = linked_id

        channel = Channel(
            name=channel_name,
            unique_id=unique_id,
            linked_id=linked_id,
            state=channel_state_desc.lower(),
            phone=phone_number,
        )

        await self.__reflector.add_channel(channel)

        if channel.unique_id == channel.linked_id or channel.linked_id in self.__origination_linked_id:
            # We create a call if the channel is root or designated as root.
            await self.__reflector.create_call(linked_id=channel.linked_id)
            try:
                self.__origination_linked_id.remove(channel.linked_id)
            except ValueError:
                pass
        else:
            await self.__reflector.add_channel_to_call(linked_id=channel.linked_id, channel_unique_id=channel.unique_id)
