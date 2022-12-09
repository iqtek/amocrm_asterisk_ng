from typing import Collection
from typing import Mapping

from asterisk_ng.interfaces import Agent, CrmUserId
from asterisk_ng.interfaces import IGetAgentCollectionQuery


__all__ = ["GetAgentCollectionQueryImpl"]


class GetAgentCollectionQueryImpl(IGetAgentCollectionQuery):

    __slots__ = (
        "__agents",
    )

    def __init__(
        self,
        agent_id_to_phone_mapping: Mapping[CrmUserId, str],
    ) -> None:
        self.__agents = [
            Agent(
                user_id=key,
                phone=value,
            )
            for key, value in agent_id_to_phone_mapping.items()
        ]

    async def __call__(self) -> Collection[Agent]:
        return self.__agents
