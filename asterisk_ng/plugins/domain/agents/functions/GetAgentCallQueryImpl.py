from typing import Mapping

from asterisk_ng.interfaces import CrmUserId
from asterisk_ng.interfaces import IGetAgentCallQuery
from asterisk_ng.interfaces import CallDomainModel

__all__ = ["GetAgentCallQueryImpl"]


class GetAgentCallQueryImpl(IGetAgentCallQuery):

    __slots__ = (
        "__agents",
    )

    def __init__(self, agents: Mapping[CrmUserId, CallDomainModel]) -> None:
        self.__agents = agents

    async def __call__(self, user_id: CrmUserId) -> CallDomainModel:
        return self.__agents[user_id]
