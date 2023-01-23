from asterisk_ng.interfaces import IHangupTelephonyCommand

from asterisk_ng.plugins.telephony.ami_manager import Action
from asterisk_ng.plugins.telephony.ami_manager import IAmiManager

from ...reflector import IReflector


__all__ = ["HangupTelephonyCommandImpl"]


class HangupTelephonyCommandImpl(IHangupTelephonyCommand):

    __slots__ = (
        "__ami_manager",
        "__reflector",
    )

    def __init__(
        self,
        ami_manager: IAmiManager,
        reflector: IReflector,
    ) -> None:
        self.__ami_manager = ami_manager
        self.__reflector = reflector

    async def __call__(
        self,
        phone_number: str,
    ) -> None:

        channel = await self.__reflector.get_channel_by_phone(phone=phone_number)

        action = Action(
            name="Hangup",
            parameters={
                "Channel": channel.name,
                "Cause": 16,
            }
        )
        await self.__ami_manager.send_action(action)
