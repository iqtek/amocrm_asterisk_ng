from .OriginationConfig import OriginationConfig
from ..core import (
    IOriginationCallCH,
    OriginationCallCommand,
)
from ......core import (
    Action,
    IAmiManager,
)


__all__ = [
    "OriginationCallCH"
]


class OriginationCallCH(IOriginationCallCH):

    def __init__(
        self,
        config: OriginationConfig,
        ami_manager: IAmiManager
    ) -> None:
        self.__config = config
        self.__ami_manager = ami_manager

    async def __call__(self, command: OriginationCallCommand) -> None:
        caller_phone_number = command.caller_phone_number
        called_phone_number = command.called_phone_number
        action = Action(
            name="Originate",
            parameters={
                "Channel": f"Local/{caller_phone_number}@{self.__config.context}",
                "Context": self.__config.context,
                "Exten": called_phone_number,
                "Async": True,
                "Priority": 1,
                "Timeout": self.__config.timeout
            }
        )
        await self.__ami_manager.send_action(action)
