from typing import Mapping

from asterisk_ng.interfaces import Agent
from asterisk_ng.interfaces import CrmUserId
from asterisk_ng.interfaces import IGetCrmUserIdByPhoneQuery


__all__ = ["GetCrmUserIdByPhoneQueryImpl"]


class GetCrmUserIdByPhoneQueryImpl(IGetCrmUserIdByPhoneQuery):

    __slots__ = (
        "__phone_to_agent_mapping",
    )

    def __init__(
        self,
        phone_to_agent_mapping: Mapping[str, Agent]
    ) -> None:
        self.__phone_to_agent_mapping = phone_to_agent_mapping

    async def __call__(self, phone: str) -> CrmUserId:
        return self.__phone_to_agent_mapping[phone].user_id
