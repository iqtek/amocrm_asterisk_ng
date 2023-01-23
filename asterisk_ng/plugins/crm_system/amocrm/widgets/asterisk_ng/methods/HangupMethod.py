from typing import Any
from typing import Mapping
from typing import Optional

from asterisk_ng.interfaces import CrmUserId
from asterisk_ng.interfaces import IHangupDomainCommand

from ..controller import IControllerMethod


__all__ = ["HangupMethod"]


class HangupMethod(IControllerMethod):

    __slots__ = (
        "__hangup_domain_command",
    )

    def __init__(
        self,
        hangup_domain_command: IHangupDomainCommand
    ) -> None:
        self.__hangup_domain_command = hangup_domain_command

    async def __call__(self, amouser_email: str, amouser_id: int) -> Optional[Mapping[str, Any]]:
        await self.__hangup_domain_command(
            user_id=CrmUserId(id=amouser_id, email=amouser_email),
        )
        return None
