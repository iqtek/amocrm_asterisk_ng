from typing import Literal

from ..core import IGetCallDirectionFunction
from ..core import IsInternalNumberFunction


__all__ = [
    "GetCallDirectionFunctionImpl",
]


class GetCallDirectionFunctionImpl(IGetCallDirectionFunction):

    __slots__ = (
        "__is_internal_number_function",
    )

    def __init__(
        self,
        is_internal_number_function: IsInternalNumberFunction,
    ) -> None:
        self.__is_internal_number_function = is_internal_number_function

    async def __call__(
        self,
        caller_phone_number: str,
        called_phone_number: str,
    ) -> Literal["inbound", "outbound"]:

        if await self.__is_internal_number_function(caller_phone_number) and \
                not await self.__is_internal_number_function(called_phone_number):
            return "outbound"

        if not await self.__is_internal_number_function(caller_phone_number) and \
                await self.__is_internal_number_function(called_phone_number):
            return "inbound"

        raise Exception("Unable to determine the direction of the call.")
