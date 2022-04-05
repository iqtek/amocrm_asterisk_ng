from asterisk_amocrm.infrastructure import IQuery


__all__ = [
    "IGetUserIdByPhoneQuery",
]


class IGetUserIdByPhoneQuery(IQuery):

    async def __call__(self, phone_number: str) -> int:
        """
        Get user is in crm by his phone number.
        :raise KeyError: If user with given number not found.
        :return: id (int)
        """
        raise NotImplementedError()
