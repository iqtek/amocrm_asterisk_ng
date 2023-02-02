from typing import Mapping
from typing import Optional

from asterisk_ng.interfaces import Agent
from asterisk_ng.interfaces import CrmContact
from asterisk_ng.interfaces import CrmUserId
from asterisk_ng.interfaces import IGetContactByPhoneQuery
from asterisk_ng.interfaces import IGetResponsibleUserByPhoneQuery


__all__ = ["GetResponsibleUserByPhoneQueryImpl"]


class GetResponsibleUserByPhoneQueryImpl(IGetResponsibleUserByPhoneQuery):

    __slots__ = (
        "__agent_id_to_phone_mapping",
        "__get_contact_by_phone_query",
        "__default_responsible_id",
    )

    def __init__(
        self,
        agent_id_to_phone_mapping: Mapping[CrmUserId, str],
        get_contact_by_phone_query: IGetContactByPhoneQuery,
        default_responsible: Optional[Agent] = None,
    ) -> None:
        self.__agent_id_to_phone_mapping = agent_id_to_phone_mapping
        self.__get_contact_by_phone_query = get_contact_by_phone_query
        self.__default_responsible_id = getattr(default_responsible, "user_id", None)

    async def __call__(self, client_phone: str) -> str:
        try:
            contact: CrmContact = await self.__get_contact_by_phone_query(phone_number=client_phone)
            user_id = contact.responsible_user_id
        except KeyError:
            user_id = self.__default_responsible_id

        if user_id is None:
            raise KeyError(f"The responsible user for `{client_phone}` has not been identified.")

        try:
            return self.__agent_id_to_phone_mapping[user_id]
        except KeyError:
            raise KeyError(f"The responsible user with id: `{user_id}` is not an agent.")
