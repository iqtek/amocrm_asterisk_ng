from typing import Dict
from ......core import GetUserEmailByPhoneQuery
from ...query_handlers import IGetUserEmailByPhoneQH
from asterisk_amocrm.infrastructure import ILogger


__all__ = [
    "GetUserEmailByPhoneQH",
]


class GetUserEmailByPhoneQH(IGetUserEmailByPhoneQH):

    def __init__(self, users: Dict[str, str], logger: ILogger) -> None:
        self.__users = users
        self.__logger = logger

    async def __call__(self, query: GetUserEmailByPhoneQuery) -> str:
        try:
            email = self.__users[query.phone_number]
            self.__logger.debug(
                f"GetUserEmailByPhoneQH: phone: {query.phone_number} "
                f"email: {email} ."
            )
            return email
        except KeyError:
            raise KeyError(
                f"GetUserEmailByPhoneQH: "
                f"No user with number '{query.phone_number}' ."
            )
