from amocrm_asterisk_ng.domain import ICrm
from amocrm_asterisk_ng.domain import RingingEvent

from ..functions import IsInternalNumberFunction


__all__ = [
    "RingingEventHandler",
]


class RingingEventHandler(IEventHandler):

    __slots__ = (
        "__crm",
        "__is_internal_number_function",
    )

    def __init__(
        self,
        crm: ICrm,
        is_internal_number_function: IsInternalNumberFunction
    ) -> None:
        self.__crm = crm
        self.__is_internal_number_function = is_internal_number_function

    async def __call__(self, event: RingingEvent) -> None:

        user_id = await self.__crm.get_user_id_by_phone(
            phone_number=event.called_phone_number,
        )

        if not await self.__is_internal_number_function(caller_phone_number):
            await self.__raise_card_command(
                phone_number=event.caller_phone_number,
                users=(user_id,)
            )
