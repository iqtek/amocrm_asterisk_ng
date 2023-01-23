from typing import Collection

from asterisk_ng.system.dispatcher import IQuery
from ..models import Agent


__all__ = ["IGetAgentCollectionQuery"]


class IGetAgentCollectionQuery(IQuery[Collection[Agent]]):

    __slots__ = ()

    async def __call__(self) -> Collection[Agent]:
        raise NotImplementedError()
