from amocrm_asterisk_ng.infrastructure import IQuery
from typing import Mapping


__all__ = [
    "IGetUsersEmailAddressesQuery",
]


class IGetUsersEmailAddressesQuery(IQuery[Mapping[str, str]]):

    __slots__ = ()

    async def __call__(self) -> Mapping[str, str]:
        """Get users' email addresses."""
        raise NotImplementedError()
