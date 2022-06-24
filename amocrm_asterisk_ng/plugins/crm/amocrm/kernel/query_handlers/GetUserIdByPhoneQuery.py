from typing import MutableMapping

from amocrm_api_client import AmoCrmApiClient

from amocrm_asterisk_ng.domain import IGetOperatorIdByPhoneQuery

from ...core import IGetOperatorsEmailAddressesQuery


__all__ = [
    "GetOperatorIdByPhoneQuery",
]


class GetOperatorIdByPhoneQuery(IGetOperatorIdByPhoneQuery):

    __slots__ = (
        "__cache",
        "__amo_client",
        "__get_users_email_addresses",
    )

    def __init__(
        self,
        amo_client: AmoCrmApiClient,
        get_users_email_addresses: IGetOperatorsEmailAddressesQuery,
    ) -> None:
        self.__cache: MutableMapping[str, int] = {}
        self.__amo_client = amo_client
        self.__get_users_email_addresses = get_users_email_addresses

    async def __call__(self, phone_number: str) -> int:
        if phone_number in self.__cache.keys():
            return self.__cache[phone_number]

        emails = await self.__get_users_email_addresses()
        try:
            email = emails[phone_number]
        except KeyError:
            raise Exception(
                f"Operator with phone: `{phone_number}` not found."
            )

        users = await self.__amo_client.users.get_page()
        for user in users.embedded:
            if user.email == email:
                self.__cache[phone_number] = user.id
                return user.id

        raise Exception(
            f"Operator with phone: `{phone_number}` not found."
        )
