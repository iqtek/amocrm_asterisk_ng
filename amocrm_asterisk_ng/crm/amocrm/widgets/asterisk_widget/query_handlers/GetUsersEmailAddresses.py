from typing import Mapping

from ....core import IGetUsersEmailAddresses


class GetUsersEmailAddresses(IGetUsersEmailAddresses):

    __slots__ = (
        "__users",
    )

    def __init__(self, users: Mapping[str, str]) -> None:
        self.__users = users

    async def __call__(self) -> Mapping[str, str]:
        return self.__users
