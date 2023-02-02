from asterisk_ng.interfaces import Agent
from asterisk_ng.system.dispatcher import IQuery


__all__ = ["IGetResponsibleAgentByPhoneQuery"]


class IGetResponsibleAgentByPhoneQuery(IQuery[Agent]):

    __slots__ = ()

    async def __call__(self, client_phone: str) -> Agent:
        raise NotImplementedError()
