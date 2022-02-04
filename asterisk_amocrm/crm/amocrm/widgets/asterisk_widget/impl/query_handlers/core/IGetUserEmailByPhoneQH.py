from asterisk_amocrm.infrastructure.dispatcher import IQueryHandler
from ......core import GetUserEmailByPhoneQuery


__all__ = [
    "IGetUserEmailByPhoneQH",
]


class IGetUserEmailByPhoneQH(IQueryHandler):

    async def __call__(self, query: GetUserEmailByPhoneQuery) -> str:
        """
        Get user email in crm by his phone number.
        :raise KeyError: If user with given number not found.
        :return: email (str)
        """
        raise NotImplementedError()
