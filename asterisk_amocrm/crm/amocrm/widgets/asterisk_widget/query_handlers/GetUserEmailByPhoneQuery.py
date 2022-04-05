from typing import Mapping
from ....core import IGetUserEmailByPhoneQuery


__all__ = [
    "GetUserEmailByPhoneQuery",
]


class GetUserEmailByPhoneQuery(IGetUserEmailByPhoneQuery):

    __slots__ = (
        "__users",
    )

    def __init__(self, users: Mapping[str, str]) -> None:
        self.__users = users

    async def __call__(self, phone_number: str) -> str:
        try:
            email = self.__users[phone_number]
            return email
        except KeyError:
            raise KeyError(
                f"GetUserEmailByPhoneQH: "
                f"No user with number '{phone_number}'."
            )
