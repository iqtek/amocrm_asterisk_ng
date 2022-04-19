from amocrm_asterisk_ng.domain import IOriginationRequestCommand
from amocrm_asterisk_ng.domain import IOriginationCallCommand

__all__ = [
    "OriginationRequestCommandImpl",
]


class OriginationRequestCommandImpl(IOriginationRequestCommand):

    __slots__ = (
        "__origination_call_command",
    )

    def __init__(
        self,
        origination_call_command: IOriginationCallCommand,
    ) -> None:
        self.__origination_call_command = origination_call_command

    async def __call__(self, caller_phone_number: str, called_phone_number: str) -> None:
        await self.__origination_call_command(caller_phone_number, called_phone_number)
