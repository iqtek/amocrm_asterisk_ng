from amocrm_asterisk_ng.domain import IGetUserIdByPhoneQuery
from amocrm_asterisk_ng.domain import RingingEvent
from amocrm_asterisk_ng.infrastructure import IEventHandler

from ..functions import IsInternalNumberFunction


__all__ = [
    "RingingEventHandler",
]


class RingingEventHandler(IEventHandler):

    __slots__ = (
        "__get_user_id_by_phone_query",
        "__is_internal_number_function",
    )

    def __init__(
        self,
        get_user_id_by_phone_query: IGetUserIdByPhoneQuery,
        is_internal_number_function: IsInternalNumberFunction
    ) -> None:
        self.__get_user_id_by_phone_query = get_user_id_by_phone_query
        self.__is_internal_number_function = is_internal_number_function

    async def __call__(self, event: RingingEvent) -> None:

        user_id = await self.__get_user_id_by_phone_query(
            phone_number=event.called_phone_number,
        )

        if not await self.__is_internal_number_function(event.called_phone_number):
            await self.__raise_card_command(
                phone_number=event.caller_phone_number,
                users=(user_id,)
            )
