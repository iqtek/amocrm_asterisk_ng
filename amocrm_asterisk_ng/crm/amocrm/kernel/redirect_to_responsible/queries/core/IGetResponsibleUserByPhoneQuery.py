from amocrm_asterisk_ng.infrastructure import IQuery


__all__ = [
    "IGetResponsibleUserByPhoneQuery",
]


class IGetResponsibleUserByPhoneQuery(IQuery[str]):

    __slots__ = ()

    async def __call__(self, phone_number: str) -> str:
        """
        Get the number of the responsible user for the customer number.

        :param phone_number: Client's phone number.
        :type phone_number: str
        :raise ResponsibleUserNotFoundException: If there is no responsible user.
        :return: responsible user phone number.
        :rtype: str
        """
        raise NotImplementedError()
