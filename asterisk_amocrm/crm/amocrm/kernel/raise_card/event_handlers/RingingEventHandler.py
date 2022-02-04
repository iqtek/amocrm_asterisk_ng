from asterisk_amocrm.domains import RingingEvent
from asterisk_amocrm.infrastructure import (
    ILogger,
    IDispatcher,
    IEventHandler,
)
from ..commands import RaiseCardCommand
from ....core import GetUserIdByPhoneQuery


__all__ = [
    "RingingEventHandler",
]


class RingingEventHandler(IEventHandler):

    def __init__(
        self,
        dispatcher: IDispatcher,
        logger: ILogger,
    ) -> None:
        self.__logger = logger
        self.__dispatcher = dispatcher

    async def __call__(self, event: RingingEvent) -> None:

        query_called_id = GetUserIdByPhoneQuery(
            phone_number=event.called_phone_number,
        )
        try:
            user_id = await self.__dispatcher.on_query(query_called_id)
        except KeyError:
            self.__logger.debug(
                "Ringing detected: "
                f"{event.caller_phone_number} -> "
                f"{event.called_phone_number}. "
                "The called has no id. The card was not raised."
            )
            return

        raise_card_command = RaiseCardCommand(
            phone_number=event.caller_phone_number,
            users=[user_id]
        )
        await self.__dispatcher.on_command(raise_card_command)
