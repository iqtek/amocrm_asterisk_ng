from asterisk_ng.system.dispatcher import IQuery

from ..models import CrmUser, CrmUserId


__all__ = ["IGetCrmUserQuery"]


class IGetCrmUserQuery(IQuery[CrmUser]):

    __slots__ = ()

    async def __call__(self, user_id: CrmUserId) -> CrmUser:
        raise NotImplementedError()
