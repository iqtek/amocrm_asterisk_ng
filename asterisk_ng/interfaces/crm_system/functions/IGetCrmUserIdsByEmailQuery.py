from typing import Collection
from typing import Mapping

from asterisk_ng.system.dispatcher import IQuery

from ..models import CrmUserId


__all__ = ["IGetCrmUserIdsByEmailQuery"]


class IGetCrmUserIdsByEmailQuery(IQuery[Mapping[str, CrmUserId]]):

    __slots__ = ()

    async def __call__(self, emails: Collection[str]) -> Mapping[str, CrmUserId]:
        raise NotImplementedError()
