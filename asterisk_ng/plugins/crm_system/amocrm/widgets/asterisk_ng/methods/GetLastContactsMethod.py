from typing import Any
from typing import Mapping
from typing import Optional
from typing import Collection
from asterisk_ng.interfaces import CrmUserId
from asterisk_ng.interfaces import IHangupDomainCommand

from .models import Contact
from ..controller import IControllerMethod


__all__ = ["GetLastContactsMethod"]


class GetLastContactsMethod(IControllerMethod):

    __slots__ = (
        "__contacts",
    )

    def __init__(self, contacts: Collection[Contact]) -> None:
        self.__contacts = contacts

    async def __call__(
        self,
        amouser_email: str,
        amouser_id: int,
        max_results: int = 100,
    ) -> Any:
        if max_results < 0:
            max_results = 100

        return tuple(map(lambda c: c.dict(), self.__contacts[0: max_results]))
