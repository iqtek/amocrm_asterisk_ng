from glassio.dispatcher import IQuery


__all__ = [
    "IGetResponsibleUserByPhoneQuery",
]


class IGetResponsibleUserByPhoneQuery(IQuery[str]):

    __slots__ = ()

    async def __call__(self, phone_number: str) -> str:
        """
        Get phone of responsible user for client`s phone_number.

        :param phone_number: client`s phone_number.
        :type phone_number: str
        :return: phone of responsible user
        :rtype: str
        """
        raise NotImplementedError()
