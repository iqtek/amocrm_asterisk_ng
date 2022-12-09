from typing import Any
from typing import Mapping
from typing import Optional

from ..controller import IControllerMethod
from ..controller import InvalidParamsException

from asterisk_ng.interfaces import ISetMuteDomainCommand
from asterisk_ng.interfaces import CrmUserId


__all__ = ["SetMuteMethod"]


class SetMuteMethod(IControllerMethod):

    __slots__ = (
        "__set_mute_domain_command",
    )

    def __init__(
        self,
        set_mute_domain_command: ISetMuteDomainCommand
    ) -> None:
        self.__set_mute_domain_command = set_mute_domain_command

    async def __call__(
        self,
        amouser_email: str,
        amouser_id: int,
        is_mute: Optional[bool] = None
    ) -> Optional[Mapping[str, Any]]:

        if is_mute is None:
            raise InvalidParamsException()

        await self.__set_mute_domain_command(
            user_id=CrmUserId(id=amouser_id, email=amouser_email),
            is_mute=is_mute,
        )
        return None
