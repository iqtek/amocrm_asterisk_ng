import re
from typing import Optional

from amocrm_asterisk_ng.domain import IsUserPhoneNumerQuery

from ..core import IsInternalNumberFunction


__all__ = [
    "IsInternalNumberFunctionImpl",
]


class IsInternalNumberFunctionImpl(IsInternalNumberFunction):

    __slots__ = (
        "__is_user_phone_number",
        "__internal_number_pattern",
    )

    def __init__(
        self,
        is_user_phone_number: IsUserPhoneNumerQuery,
        internal_number_pattern: Optional[str],
    ) -> None:
        self.__is_user_phone_number = is_user_phone_number
        self.__internal_number_pattern = internal_number_pattern

    async def __call__(self, phone_number: str) -> bool:

        is_user_phone_number = await self.__is_user_phone_number(phone_number)
        is_corresponds_pattern = False

        if self.__internal_number_pattern is not None:
            try:
                pattern = re.compile(self.__internal_number_pattern)
                result = re.match(pattern, phone_number)
                if result is not None:
                    is_corresponds_pattern = True
            except Exception:
                pass

        return is_corresponds_pattern or is_user_phone_number
