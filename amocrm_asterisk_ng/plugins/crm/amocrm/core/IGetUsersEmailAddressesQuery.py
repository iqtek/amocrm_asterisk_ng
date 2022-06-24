from typing import Mapping

from glassio.dispatcher import IQuery


__all__ = [
    "IGetOperatorsEmailAddressesQuery",
]


class IGetOperatorsEmailAddressesQuery(IQuery[Mapping[str, str]]):

    __slots__ = ()

    async def __call__(self) -> Mapping[str, str]:
        """
        Get users' email addresses.

        Example `{"111": "address@email.com"}`.
        Getting the phone number to match the email.
        """
        raise NotImplementedError()
