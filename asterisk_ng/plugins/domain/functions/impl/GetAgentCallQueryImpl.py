from typing import Mapping

from asterisk_ng.interfaces import CallDomainModel
from asterisk_ng.interfaces import CrmUserId
from asterisk_ng.interfaces import IGetAgentCallQuery


__all__ = ["GetAgentCallQueryImpl"]


class GetAgentCallQueryImpl(IGetAgentCallQuery):

    __slots__ = (
        "__active_calls",
    )

    def __init__(self, active_calls: Mapping[CrmUserId, CallDomainModel]) -> None:
        self.__active_calls = active_calls

    async def __call__(self, user_id: CrmUserId) -> CallDomainModel:
        return self.__active_calls[user_id]
