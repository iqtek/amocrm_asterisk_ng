from datetime import datetime

from asterisk_ng.interfaces import IRedirectTelephonyCommand

from asterisk_ng.plugins.telephony.ami_manager import Action
from asterisk_ng.plugins.telephony.ami_manager import IAmiManager

from asterisk_ng.system.event_bus import IEventBus

from ...reflector import IReflector


__all__ = ["RedirectTelephonyCommandImpl"]


class RedirectTelephonyCommandImpl(IRedirectTelephonyCommand):

    __slots__ = (
        "__ami_manager",
        "__reflector",
        "__event_bus",
        "__context",
    )

    def __init__(
        self,
        ami_manager: IAmiManager,
        reflector: IReflector,
        event_bus: IEventBus,
        context: str
    ) -> None:
        self.__ami_manager = ami_manager
        self.__reflector = reflector
        self.__event_bus = event_bus
        self.__context = context

    async def __call__(
        self,
        phone_number: str,
        redirect_phone_number: str,
    ) -> None:
        channel = await self.__reflector.get_channel_by_phone(phone=phone_number)

        action = Action(
            name="Redirect",
            parameters={
                "Channel": channel.name,
                "Exten": redirect_phone_number,
                "Context": self.__context,
                "Priority": 1,
            }
        )
        await self.__ami_manager.send_action(action)
