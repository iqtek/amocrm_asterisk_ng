from typing import Mapping

from amocrm_asterisk_ng.domain import IsUserPhoneNumerQuery


__all__ = [
    "IsUserPhoneNumerQueryImpl",
]


class IsUserPhoneNumerQueryImpl(IsUserPhoneNumerQuery):

    __slots__ = (
        "__users",
    )

    def __init__(self, users: Mapping[str, str]) -> None:
        self.__users = users

    async def __call__(self, phone_number: str) -> bool:
        return phone_number in self.__users.keys()
