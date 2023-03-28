from typing import Mapping

from asterisk_ng.interfaces import Agent
from asterisk_ng.interfaces import CrmContact
from asterisk_ng.interfaces import CrmUserId
from asterisk_ng.interfaces import IGetContactByPhoneQuery

from ..core import IGetResponsibleAgentByPhoneQuery


__all__ = ["GetResponsibleAgentByPhoneQueryImpl"]


class GetResponsibleAgentByPhoneQueryImpl(IGetResponsibleAgentByPhoneQuery):

    __slots__ = (
        "__user_id_to_agent_mapping",
        "__get_contact_by_phone_query",
    )

    def __init__(
        self,
        user_id_to_agent_mapping: Mapping[CrmUserId, Agent],
        get_contact_by_phone_query: IGetContactByPhoneQuery,
    ) -> None:
        self.__user_id_to_agent_mapping = user_id_to_agent_mapping
        self.__get_contact_by_phone_query = get_contact_by_phone_query

    async def __call__(self, client_phone: str) -> Agent:
        try:
            contact: CrmContact = await self.__get_contact_by_phone_query(phone_number=client_phone)
        except KeyError as exc:
            raise KeyError(f"The responsible user for `{client_phone}` has not been identified.") from exc

        return self.__user_id_to_agent_mapping[contact.responsible_user_id]
