from asterisk_ng.system.dispatcher import IQuery

from ...crm_system import CrmUserId


__all__ = ["IGetCrmUserIdByPhoneQuery"]


class IGetCrmUserIdByPhoneQuery(IQuery[CrmUserId]):

    __slots__ = ()

    async def __call__(self, phone: str) -> CrmUserId:
        raise NotImplementedError()
