from typing import Collection

from asterisk_ng.interfaces import Agent
from asterisk_ng.interfaces import IGetAgentCollectionQuery


__all__ = ["GetAgentCollectionQueryImpl"]


class GetAgentCollectionQueryImpl(IGetAgentCollectionQuery):

    __slots__ = (
        "__agents",
    )

    def __init__(
        self,
        agents: Collection[Agent],
    ) -> None:
        self.__agents = tuple(agents)

    async def __call__(self) -> Collection[Agent]:
        return self.__agents
