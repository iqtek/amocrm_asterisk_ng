from typing import MutableMapping

from amocrm_api_client import AmoCrmApiClient

from amocrm_asterisk_ng.domain import IGetUserIdByPhoneQuery

from ...core import IGetUsersEmailAddressesQuery


__all__ = [
    "GetUserIdByPhoneQuery",
]


class GetUserIdByPhoneQuery(IGetUserIdByPhoneQuery):

    __slots__ = (
        "__cache",
        "__amo_client",
        "__get_users_email_addresses",
    )

    def __init__(
        self,
        amo_client: AmoCrmApiClient,
        get_users_email_addresses: IGetUsersEmailAddressesQuery,
    ) -> None:
        self.__cache: MutableMapping[str, int] = {}
        self.__amo_client = amo_client
        self.__get_users_email_addresses = get_users_email_addresses

    async def __call__(self, phone_number: str) -> int:
        try:
            return self.__cache[phone_number]
        except KeyError:
            pass

        emails = await self.__get_users_email_addresses()
        if phone_number not in emails.keys():
            raise KeyError(
                f"User with phone: '{phone_number}' not found."
            )

        email = emails[phone_number]

        users = await self.__amo_client.users.get_page()

        for user in users.embedded:
            if user.email == email:
                self.__cache[phone_number] = user.id
                return user.id

        raise KeyError(
            f"User with phone: '{phone_number}' not found."
        )
