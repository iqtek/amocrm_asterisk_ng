from typing import Collection

from asterisk_ng.system.dispatcher import ICommand

from ..models import CrmUserId
from ..models import CrmCallDirection
from ..models import CrmCallResult


__all__ = ["ILogCallCrmCommand"]


class ILogCallCrmCommand(ICommand):

    __slots__ = ()

    async def __call__(
        self,
        unique_id: str,
        phone_number: str,
        phone_number2: str,
        direction: CrmCallDirection,
        duration: int,
        call_result: CrmCallResult,
        responsible_user_id: CrmUserId,
    ) -> None:
        raise NotImplementedError()
