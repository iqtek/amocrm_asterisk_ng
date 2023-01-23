from typing import Any
from typing import Mapping
from typing import Optional
from typing import Collection

from ..controller import IControllerMethod
from ..controller import InvalidParamsException

from asterisk_ng.interfaces import IOriginationDomainCommand
from asterisk_ng.interfaces import CrmUserId

from .models import Contact

__all__ = ["OriginationByContactMethod"]


class OriginationByContactMethod(IControllerMethod):

    __slots__ = (
        "__origination_domain_command",
        "__contacts",
    )

    def __init__(
        self,
        contacts: Mapping[int, Contact],
        origination_domain_command: IOriginationDomainCommand,
    ) -> None:
        self.__origination_domain_command = origination_domain_command
        self.__contacts = contacts

    async def __call__(
        self,
        amouser_email: str,
        amouser_id: int,
        contact_uuid: Optional[str] = None,
    ) -> Optional[Mapping[str, Any]]:

        if contact_uuid is None:
            raise InvalidParamsException()

        contact = self.__contacts[int(contact_uuid)]

        await self.__origination_domain_command(
            user_id=CrmUserId(id=amouser_id, email=amouser_email),
            phone_number=contact.phone,
        )
        return None
