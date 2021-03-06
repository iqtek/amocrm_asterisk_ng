from typing import Literal

from glassio.dispatcher import IQuery


__all__ = [
    "INormalizePhoneFunction",
]


class INormalizePhoneFunction(IQuery[str]):

    __slots__ = ()

    async def __call__(self, phone_number: str) -> str:
        raise NotImplementedError()
