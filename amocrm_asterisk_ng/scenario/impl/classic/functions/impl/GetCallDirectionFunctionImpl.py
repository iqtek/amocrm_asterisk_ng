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

    def __call__(
        self,
        caller_phone_number: str,
        called_phone_number: str,
    ) -> Literal["inbound", "outbound"]:

        if self.__is_internal_number_function(caller_phone_number) and \
                not self.__is_internal_number_function(called_phone_number):
            return "outbound"

        if not self.__is_internal_number_function(caller_phone_number) and \
                self.__is_internal_number_function(called_phone_number):
            return "inbound"

        raise Exception("Unable to determine the direction of the call.")
