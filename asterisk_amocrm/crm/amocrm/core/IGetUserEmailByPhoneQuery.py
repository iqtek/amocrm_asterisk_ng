from asterisk_amocrm.infrastructure import IQuery


__all__ = [
    "IGetUserEmailByPhoneQuery",
]


class IGetUserEmailByPhoneQuery(IQuery):

    __slots__ = ()

    async def __call__(self, phone_number: str) -> str:
        """
        Get user email in crm by his phone number.
        :raise KeyError: If user with given number not found.
        :return: email (str)
        """
        raise NotImplementedError()
