from amocrm_asterisk_ng.domain import RingingEvent
from amocrm_asterisk_ng.infrastructure import IDispatcher
from amocrm_asterisk_ng.infrastructure import IEventHandler
from amocrm_asterisk_ng.infrastructure import ILogger

from ..commands import IRaiseCardCommand
from ....core import IGetUserIdByPhoneQuery


__all__ = [
    "RingingEventHandler",
]


class RingingEventHandler(IEventHandler):

    __slots__ = (
        "__get_user_id_by_phone_query",
        "__raise_card_command",
        "__logger",
    )

    def __init__(
        self,
        get_user_id_by_phone_query: IGetUserIdByPhoneQuery,
        raise_card_command: IRaiseCardCommand,
        logger: ILogger,
    ) -> None:
        self.__get_user_id_by_phone_query = get_user_id_by_phone_query
        self.__raise_card_command = raise_card_command
        self.__logger = logger

    async def __call__(self, event: RingingEvent) -> None:

        try:
            user_id = await self.__get_user_id_by_phone_query(
                phone_number=event.called_phone_number,
            )
        except KeyError:
            self.__logger.info(
                "Ringing detected: "
                f"{event.caller_phone_number} -> "
                f"{event.called_phone_number}. "
                "The called has no id. The card was not raised."
            )
            return

        await self.__raise_card_command(
            phone_number=event.caller_phone_number,
            users=(user_id,)
        )
