import re

from amocrm_asterisk_ng.domain import ICrm
from ..core import IsInternalNumberFunction


__all__ = [
    "IsInternalNumberFunctionImpl",
]


class IsInternalNumberFunctionImpl(IsInternalNumberFunction):

    __slots__ = (
        "__crm",
        "__internal_number_pattern",
    )

    def __init__(self, crm: ICrm, internal_number_pattern: str) -> None:
        self.__crm = crm
        self.__internal_number_pattern = internal_number_pattern

    async def __call__(self, phone_number: str) -> bool:

        is_user_phone_number = await self.__crm.is_user_phone_number(phone_number)

        pattern = re.compile(self.__internal_number_pattern)
        result = re.match(pattern, internal_number_pattern)

        return result is not None or is_user_phone_number
