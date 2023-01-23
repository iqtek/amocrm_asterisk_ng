from asyncio import Future
from typing import MutableMapping

from asterisk_ng.interfaces import CrmUserId
from asterisk_ng.interfaces import CallDomainModel
from asterisk_ng.interfaces import IAwaitAgentCallChangeQuery


__all__ = ["AwaitAgentCallChangeQueryImpl"]


class AwaitAgentCallChangeQueryImpl(IAwaitAgentCallChangeQuery):

    __slots__ = (
        "__futures",
    )

    def __init__(self) -> None:
        self.__futures: MutableMapping[CrmUserId, Future[CallDomainModel]] = {}

    def pop_agents_status(self, user_id: CrmUserId) -> None:

        if user_id not in self.__futures.keys():
            return

        if self.__futures[user_id].done():
            del self.__futures[user_id]

        if user_id in self.__futures.keys():
            self.__futures[user_id].set_exception(KeyError())

    def set_agents_status(self, user_id: CrmUserId, call: CallDomainModel) -> None:
        if user_id not in self.__futures.keys():
            return

        if self.__futures[user_id].done():
            self.__futures.pop(user_id, None)
            return

        if user_id in self.__futures.keys():
            self.__futures[user_id].set_result(call)

    async def __call__(self, user_id: CrmUserId) -> CallDomainModel:
        if user_id not in self.__futures.keys():
            self.__futures[user_id] = Future()

        if self.__futures[user_id].done():
            self.__futures[user_id] = Future()

        return await self.__futures[user_id]
