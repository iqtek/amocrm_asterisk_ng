from asterisk_ng.system.dispatcher import IQuery

from ..models import CallDomainModel
from ...crm_system import CrmUserId


__all__ = ["IAwaitAgentCallChangeQuery"]


class IAwaitAgentCallChangeQuery(IQuery[CallDomainModel]):

    __slots__ = ()

    async def __call__(self, user_id: CrmUserId) -> CallDomainModel:
        raise NotImplementedError()
