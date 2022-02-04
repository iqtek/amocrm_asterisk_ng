from asterisk_amocrm.infrastructure.dispatcher import IQueryHandler
from ....core import GetUserIdByPhoneQuery


__all__ = [
    "IGetUserIdByPhoneQH",
]


class IGetUserIdByPhoneQH(IQueryHandler):

    async def __call__(self, query: GetUserIdByPhoneQuery) -> int:
        """
        Get user is in crm by his phone number.
        :raise KeyError: If user with given number not found.
        :return: id (int)
        """
        raise NotImplementedError()
