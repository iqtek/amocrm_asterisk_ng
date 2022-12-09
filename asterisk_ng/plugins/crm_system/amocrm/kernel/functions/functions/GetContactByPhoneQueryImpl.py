from amocrm_api_client import AmoCrmApiClient
from amocrm_api_client.make_amocrm_request.core import EntityNotFoundException
from amocrm_api_client.models import Contact

from asterisk_ng.interfaces import CrmContact
from asterisk_ng.interfaces import CrmUserId
from asterisk_ng.interfaces import IGetContactByPhoneQuery

__all__ = ["GetContactByPhoneQueryImpl"]


class GetContactByPhoneQueryImpl(IGetContactByPhoneQuery):

    __slots__ = (
        "__amo_client",
    )

    def __init__(self, amo_client: AmoCrmApiClient) -> None:
        self.__amo_client = amo_client

    async def __call__(self, phone_number: str) -> CrmContact:
        try:
            contact: Contact = (await self.__amo_client.contacts.smart_redirect(phone_number))[0]
        except EntityNotFoundException:
            raise KeyError(f"Contact by phone: `{phone_number}`not found.")
        else:
            return CrmContact(
                id=contact.id,
                responsible_user_id=CrmUserId(id=contact.responsible_user_id),
                name=contact.name,
                first_name=contact.first_name,
                last_name=contact.last_name,
            )
