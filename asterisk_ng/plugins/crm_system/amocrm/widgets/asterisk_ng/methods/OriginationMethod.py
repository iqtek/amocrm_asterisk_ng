from typing import Any
from typing import Mapping
from typing import Optional

from ..controller import IControllerMethod
from ..controller import InvalidParamsException

from asterisk_ng.interfaces import IOriginationDomainCommand
from asterisk_ng.interfaces import CrmUserId


__all__ = ["OriginationMethod"]


class OriginationMethod(IControllerMethod):

    __slots__ = (
        "__origination_domain_command",
    )

    def __init__(
        self,
        origination_domain_command: IOriginationDomainCommand
    ) -> None:
        self.__origination_domain_command = origination_domain_command

    async def __call__(
        self,
        amouser_email: str,
        amouser_id: int,
        phone: Optional[str] = None,
    ) -> Optional[Mapping[str, Any]]:

        if phone is None:
            raise InvalidParamsException()

        await self.__origination_domain_command(
            user_id=CrmUserId(id=amouser_id, email=amouser_email),
            phone_number=phone,
        )
        return None
