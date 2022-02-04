from amo_crm_api_client import AmoCrmApiClient
from asterisk_amocrm.infrastructure import IDispatcher
from ..core import IGetUserIdByPhoneQH
from ....core import GetUserEmailByPhoneQuery, GetUserIdByPhoneQuery


__all__ = [
    "GetUserIdByPhoneQH",
]


class GetUserIdByPhoneQH(IGetUserIdByPhoneQH):

    def __init__(
        self,
        amo_client: AmoCrmApiClient,
        dispatcher: IDispatcher,
    ) -> None:
        self.__data = {}
        self.__amo_client = amo_client
        self.__dispatcher = dispatcher

    async def __call__(self, query: GetUserIdByPhoneQuery) -> int:
        try:
            return self.__data[query.phone_number]
        except KeyError:
            pass
        email_query = GetUserEmailByPhoneQuery(
            phone_number=query.phone_number
        )
        try:
            email = await self.__dispatcher.on_query(email_query)
        except KeyError:
            raise KeyError(
                f"User with phone: '{query.phone_number}' not found."
            )
        users = await self.__amo_client.users.get_all()
        for user in users.embedded.users:
            if user.email == email:
                self.__data[query.phone_number] = user.id
                return user.id
        raise KeyError(
            f"User with phone: '{query.phone_number}' not found."
        )
