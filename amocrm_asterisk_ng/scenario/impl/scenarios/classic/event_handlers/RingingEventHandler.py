from glassio.event_bus import IEventHandler

from amocrm_asterisk_ng.domain import IGetUserIdByPhoneQuery
from amocrm_asterisk_ng.domain import IRaiseCardCommand
from amocrm_asterisk_ng.domain import RingingEvent

from ..functions import IsInternalNumberFunction
from ..functions import INormalizePhoneFunction


__all__ = [
    "RingingEventHandler",
]


class RingingEventHandler(IEventHandler):

    __slots__ = (
        "__get_user_id_by_phone_query",
        "__is_internal_number_function",
        "__raise_card_command",
        "__normalize_phone_function",
    )

    def __init__(
        self,
        get_user_id_by_phone_query: IGetUserIdByPhoneQuery,
        is_internal_number_function: IsInternalNumberFunction,
        raise_card_command: IRaiseCardCommand,
        normalize_phone_function: INormalizePhoneFunction,
    ) -> None:
        self.__get_user_id_by_phone_query = get_user_id_by_phone_query
        self.__is_internal_number_function = is_internal_number_function
        self.__raise_card_command = raise_card_command
        self.__normalize_phone_function = normalize_phone_function

    async def __call__(self, event: RingingEvent) -> None:

        try:
            user_id = await self.__get_user_id_by_phone_query(
                phone_number=event.called_phone_number,
            )
        except Exception:
            # is not internal call
            return

        external_phone_number = await self.__normalize_phone_function(event.caller_phone_number)
        if not await self.__is_internal_number_function(external_phone_number):
            await self.__raise_card_command(
                phone_number=external_phone_number,
                users=(user_id,)
            )
