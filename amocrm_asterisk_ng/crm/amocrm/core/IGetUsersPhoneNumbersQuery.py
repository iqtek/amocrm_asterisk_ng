from typing import Mapping

from amocrm_asterisk_ng.infrastructure import IQuery


__all__ = [
    "IGetUsersPhoneNumbersQuery",
]


class IGetUsersPhoneNumbersQuery(IQuery[Mapping[str, str]]):

    __slots__ = ()

    async def __call__(self) -> Mapping[str, str]:
        """
        Get users' phone numbers.

        :return: Mapping[phone_nuber, email].
        :rtype Mapping[str, str]
        """
        raise NotImplementedError()
