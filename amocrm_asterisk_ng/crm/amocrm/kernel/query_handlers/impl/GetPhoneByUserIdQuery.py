from typing import MutableMapping

from amo_crm_api_client import AmoCrmApiClient

from ....core import IGetPhoneByUserIdQuery
from ....core import IGetUsersEmailAddresses


__all__ = [
    "GetPhoneByUserIdQuery",
]


class GetPhoneByUserIdQuery(IGetPhoneByUserIdQuery):

    __slots__ = (
        "__cache",
        "__amo_client",
        "__get_users_email_addresses",
    )

    def __init__(
        self,
        amo_client: AmoCrmApiClient,
        get_users_email_addresses: IGetUsersEmailAddresses,
    ) -> None:
        self.__cache: Optional[MutableMapping[int, str]] = None
        self.__amo_client = amo_client
        self.__get_users_email_addresses = get_users_email_addresses

    async def __initialize(self) -> None:
        self.__cache = {}

        users_with_email = await self.__get_users_email_addresses()

        amo_users = await self.__amo_client.users.get_all()

        for phone, email in users_with_email.items():
            for user in amo_users.embedded.users:
                if user.email == email:
                    self.__cache[user.id] = phone

    async def __call__(self, user_id: int) -> str:
        if self.__cache is None:
            await self.__initialize()

        return self.__cache[user_id]
