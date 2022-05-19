from glassio.dispatcher import IQuery


__all__ = [
    "IGetUserIdByPhoneQuery",
]


class IGetUserIdByPhoneQuery(IQuery[int]):

    __slots__ = ()

    async def __call__(self, phone_number: str) -> int:
        """
        Get user id by hid phone_number.

        :param phone_number: user phone_number.
        :type phone_number: str
        :raise Exception: If user not found.
        :return: user id
        :rtype: int
        """
        raise NotImplementedError()
