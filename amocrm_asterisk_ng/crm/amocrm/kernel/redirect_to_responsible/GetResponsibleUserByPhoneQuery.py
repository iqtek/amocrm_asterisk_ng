from typing import MutableMapping

from amocrm_api_client import AmoCrmApiClient
from amocrm_api_client.models import Contact
from amocrm_api_client.models import Page

from amocrm_asterisk_ng.domain import IGetResponsibleUserByPhoneQuery

from ...core import IGetPhoneByUserIdQuery


__all__ = [
    "GetResponsibleUserByPhoneQuery",
]


class GetResponsibleUserByPhoneQuery(IGetResponsibleUserByPhoneQuery):

    __slots__ = (
        "__cache",
        "__amo_client",
        "__get_phone_by_user_id_query",
    )

    def __init__(
        self,
        amo_client: AmoCrmApiClient,
        get_phone_by_user_id_query: IGetPhoneByUserIdQuery,
    ) -> None:
        self.__cache: MutableMapping[str, int] = {}
        self.__amo_client = amo_client
        self.__get_phone_by_user_id_query = get_phone_by_user_id_query

    async def __call__(self, phone_number: str) -> str:

        if phone_number is self.__cache.keys():
            user_id = self.__cache[phone_number]
            return await self.__get_phone_by_user_id_query(user_id)

        contacts_page: Page[Contact] = await self.__amo_client.contacts.get_page()

        for contact in contacts_page.embedded:
            if contact.custom_fields_values is not None:
                if contact.custom_fields_values[0].values[0].value == phone_number:
                    self.__cache[phone_number] = contact.responsible_user_id
                    user_id = contact.responsible_user_id
                    break
        else:
            raise Exception(
                f"Responsible user not found for phone_number: `{phone_number}`."
            )

        phone = await self.__get_phone_by_user_id_query(user_id)
        return phone
