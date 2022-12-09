from asterisk_ng.interfaces import IOriginationTelephonyCommand

from asterisk_ng.plugins.telephony.ami_manager import Action
from asterisk_ng.plugins.telephony.ami_manager import IAmiManager


__all__ = ["OriginationTelephonyCommandImpl"]


class OriginationTelephonyCommandImpl(IOriginationTelephonyCommand):

    __slots__ = (
        "__ami_manager",
        "__context",
        "__timeout",
    )

    def __init__(
        self,
        ami_manager: IAmiManager,
        context: str = "from-internal",
        timeout: int = 30000,
    ) -> None:
        self.__ami_manager = ami_manager
        self.__context = context
        self.__timeout = timeout

    async def __call__(
        self,
        caller_phone_number: str,
        called_phone_number: str,
    ) -> None:
        action = Action(
            name="Originate",
            parameters={
                "Channel": f"Local/{caller_phone_number}@{self.__context}",
                "Context": self.__context,
                "Exten": called_phone_number,
                "CallerID": f'"{called_phone_number}"',
                "Async": True,
                "Priority": 1,
                "Timeout": self.__timeout
            }
        )
        await self.__ami_manager.send_action(action)
