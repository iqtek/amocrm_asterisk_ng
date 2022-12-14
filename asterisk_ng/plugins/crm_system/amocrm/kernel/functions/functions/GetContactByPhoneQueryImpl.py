from re import search

from typing import Collection

from amocrm_api_client import AmoCrmApiClient
from amocrm_api_client.make_amocrm_request.core import EntityNotFoundException
from amocrm_api_client.models import Contact

from asterisk_ng.interfaces import CrmContact
from asterisk_ng.interfaces import CrmUserId
from asterisk_ng.interfaces import IGetContactByPhoneQuery

__all__ = ["GetContactByPhoneQueryImpl"]


class GetContactByPhoneQueryImpl(IGetContactByPhoneQuery):

    __POSSIBLE_PREFIXES = ("+7", "7", "8")

    __slots__ = (
        "__amo_client",
    )

    def __init__(self, amo_client: AmoCrmApiClient) -> None:
        self.__amo_client = amo_client

    def __get_possible_numbers(self, phone: str) -> Collection[str]:
        results = search("(\\d{10})$", phone)

        if results is None:
            return phone,

        return [prefix + results[0] for prefix in self.__POSSIBLE_PREFIXES]

    async def __call__(self, phone_number: str) -> CrmContact:

        possible_numbers = self.__get_possible_numbers(phone_number)

        for possible_number in possible_numbers:
            try:
                contact: Contact = (await self.__amo_client.contacts.smart_redirect(possible_number))[0]
            except EntityNotFoundException:
                continue
            else:
                return CrmContact(
                    id=contact.id,
                    responsible_user_id=CrmUserId(id=contact.responsible_user_id),
                    name=contact.name,
                    first_name=contact.first_name,
                    last_name=contact.last_name,
                )

        raise KeyError(f"Contact by phone: `{phone_number}`not found.")
