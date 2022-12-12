from typing import Mapping

from asterisk_ng.interfaces import CrmUserId
from asterisk_ng.interfaces import IGetCrmUserIdByPhoneQuery


__all__ = ["GetCrmUserIdByPhoneQueryImpl"]


class GetCrmUserIdByPhoneQueryImpl(IGetCrmUserIdByPhoneQuery):

    __slots__ = (
        "__user_phones",
    )

    def __init__(
        self,
        user_phones: Mapping[str, CrmUserId]
    ) -> None:
        self.__user_phones = user_phones

    async def __call__(self, phone: str) -> CrmUserId:
        return self.__user_phones[phone]
