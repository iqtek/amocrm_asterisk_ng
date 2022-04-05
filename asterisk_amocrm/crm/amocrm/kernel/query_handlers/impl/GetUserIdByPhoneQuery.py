from typing import MutableMapping

from amo_crm_api_client import AmoCrmApiClient
from amo_crm_api_client.exceptions import AmocrmClientException
from asterisk_amocrm.infrastructure import IDispatcher

from ....core import IGetUserIdByPhoneQuery
from ....core import IGetUserEmailByPhoneQuery


__all__ = [
    "GetUserIdByPhoneQuery",
]


class GetUserIdByPhoneQuery(IGetUserIdByPhoneQuery):

    __slots__ = (
        "__cache",
        "__amo_client",
        "__get_user_email_by_phone_query",
    )

    def __init__(
        self,
        amo_client: AmoCrmApiClient,
        get_user_email_by_phone_query: IGetUserEmailByPhoneQuery,
    ) -> None:
        self.__cache: MutableMapping[str, int] = {}
        self.__amo_client = amo_client
        self.__get_user_email_by_phone_query = get_user_email_by_phone_query

    async def __call__(self, phone_number: str) -> int:
        try:
            return self.__cache[phone_number]
        except KeyError:
            pass

        try:
            email = await self.__get_user_email_by_phone_query(
                phone_number=phone_number,
            )
        except KeyError:
            raise KeyError(
                f"User with phone: '{phone_number}' not found."
            )

        users = await self.__amo_client.users.get_all()

        for user in users.embedded.users:
            if user.email == email:
                self.__cache[phone_number] = user.id
                return user.id

        raise KeyError(
            f"User with phone: '{phone_number}' not found."
        )
