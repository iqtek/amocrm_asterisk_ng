from amocrm_asterisk_ng.infrastructure import IQuery
from typing import Mapping


__all__ = [
    "IGetUsersEmailAddresses",
]


class IGetUsersEmailAddresses(IQuery):

    __slots__ = ()

    async def __call__(self) -> Mapping[str, str]:
        """Get users' email addresses."""
        raise NotImplementedError()
