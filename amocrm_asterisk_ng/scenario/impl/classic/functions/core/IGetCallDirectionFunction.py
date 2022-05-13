from typing import Literal

from glassio.dispatcher import IQuery


__all__ = [
    "IGetCallDirectionFunction",
]


class IGetCallDirectionFunction(IQuery[Literal["inbound", "outbound"]]):

    __slots__ = ()

    async def __call__(
        self,
        caller_phone_number: str,
        called_phone_number: str,
    ) -> Literal["inbound", "outbound"]:
        raise NotImplementedError()
