from typing import Any
from typing import Mapping
from typing import Optional

from asterisk_ng.interfaces import CrmUserId
from asterisk_ng.interfaces import IRedirectDomainCommand

from ..controller import IControllerMethod
from ..controller import InvalidParamsException


__all__ = ["RedirectMethod"]


class RedirectMethod(IControllerMethod):

    __slots__ = (
        "__redirect_domain_command",
    )

    def __init__(
        self,
        redirect_domain_command: IRedirectDomainCommand
    ) -> None:
        self.__redirect_domain_command = redirect_domain_command

    async def __call__(
        self,
        amouser_email: str,
        amouser_id: int,
        phone: Optional[str] = None,
    ) -> Optional[Mapping[str, Any]]:

        if phone is None:
            raise InvalidParamsException()

        await self.__redirect_domain_command(
            user_id=CrmUserId(id=amouser_id, email=amouser_email),
            phone_number=phone,
        )
        return None
