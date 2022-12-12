from typing import Collection
from typing import Mapping

from asterisk_ng.system.dispatcher import IQuery

from ..models import CrmUser


__all__ = ["IGetCrmUsersByEmailsQuery"]


class IGetCrmUsersByEmailsQuery(IQuery[Mapping[str, CrmUser]]):

    __slots__ = ()

    async def __call__(self, emails: Collection[str]) -> Mapping[str, CrmUser]:
        raise NotImplementedError()
