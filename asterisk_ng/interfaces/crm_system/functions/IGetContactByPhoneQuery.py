from asterisk_ng.system.dispatcher import IQuery

from ..models import CrmContact


__all__ = ["IGetContactByPhoneQuery"]


class IGetContactByPhoneQuery(IQuery[CrmContact]):

    __slots__ = ()

    async def __call__(self, phone_number: str) -> CrmContact:
        raise NotImplementedError()
