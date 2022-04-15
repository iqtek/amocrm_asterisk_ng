from typing import Literal


__all__ = [
    "IGetCallDirectionFunction",
]


class IGetCallDirectionFunction:

    __slots__ = ()

    def __call__(
        self,
        caller_phone_number: str,
        called_phone_number: str,
    ) -> Literal["inbound", "outbound"]:
        raise NotImplementedError()
