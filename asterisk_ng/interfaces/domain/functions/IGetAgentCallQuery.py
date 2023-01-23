from asterisk_ng.system.dispatcher import IQuery

from ..models import CallDomainModel
from ...crm_system import CrmUserId


__all__ = ["IGetAgentCallQuery"]


class IGetAgentCallQuery(IQuery[CallDomainModel]):

    __slots__ = ()

    async def __call__(self, agent_id: CrmUserId) -> CallDomainModel:
        raise NotImplementedError()
