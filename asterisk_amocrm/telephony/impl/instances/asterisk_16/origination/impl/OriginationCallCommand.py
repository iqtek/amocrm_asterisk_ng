from .OriginationConfig import OriginationConfig
from ..core import IOriginationCallCommand
from ......core import Action
from ......core import IAmiManager


__all__ = [
    "OriginationCallCommand"
]


class OriginationCallCommand(IOriginationCallCommand):

    __slots__ = (
        "__config",
        "__ami_manager",
    )

    def __init__(
        self,
        config: OriginationConfig,
        ami_manager: IAmiManager
    ) -> None:
        self.__config = config
        self.__ami_manager = ami_manager

    async def __call__(
        self,
        caller_phone_number: str,
        called_phone_number: str,
    ) -> None:
        # "CallerID": f' "{called_phone_number}',
        action = Action(
            name="Originate",
            parameters={
                "Channel": f"Local/{caller_phone_number}@{self.__config.context}",
                "Context": self.__config.context,
                "Exten": called_phone_number,
                "CallerID": f'"{called_phone_number}"',
                "Async": True,
                "Priority": 1,
                "Timeout": self.__config.timeout
            }
        )
        await self.__ami_manager.send_action(action)
