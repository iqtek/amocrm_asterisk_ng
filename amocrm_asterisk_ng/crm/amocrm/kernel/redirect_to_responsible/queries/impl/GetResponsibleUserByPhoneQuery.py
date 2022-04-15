from amo_crm_api_client import AmoCrmApiClient
from amo_crm_api_client.exceptions import AmocrmClientException
from amo_crm_api_client.repositories.core.models import ContactsPage

from ..core import IGetResponsibleUserByPhoneQuery
from ..core import ResponsibleUserNotFoundException
from .....core import IGetPhoneByUserIdQuery


__all__ = [
    "GetResponsibleUserByPhoneQuery",
]


class GetResponsibleUserByPhoneQuery(IGetResponsibleUserByPhoneQuery):

    __slots__ = (
        "__amo_client",
        "__get_phone_by_user_id_query",
    )

    def __init__(
        self,
        amo_client: AmoCrmApiClient,
        get_phone_by_user_id_query: IGetPhoneByUserIdQuery,
    ) -> None:
        self.__amo_client = amo_client
        self.__get_phone_by_user_id_query = get_phone_by_user_id_query

    async def __call__(self, phone_number: str) -> str:
        try:
            contacts_page: ContactsPage = await self.__amo_client.contacts.get_page_by_phone_number(
                phone_number=phone_number,
            )
        except AmocrmClientException:
            raise ResponsibleUserNotFoundException()

        for contact in contacts_page.embedded.contacts:
            if contact.custom_fields_values[0].values[0].value == phone_number:
                user_id = contact.responsible_user_id
                break
        else:
            raise ResponsibleUserNotFoundException()

        try:
            phone = await self.__get_phone_by_user_id_query(
                user_id=user_id,
            )
        except KeyError:
            raise ResponsibleUserNotFoundException()

        return phone
