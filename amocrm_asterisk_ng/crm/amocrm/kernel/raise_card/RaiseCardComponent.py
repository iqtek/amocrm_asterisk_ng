from amo_crm_api_client import AmoCrmApiClient

from amocrm_asterisk_ng.infrastructure import IDispatcher
from amocrm_asterisk_ng.infrastructure import IEventBus
from amocrm_asterisk_ng.infrastructure import ILogger
from amocrm_asterisk_ng.infrastructure import InitializableComponent

from ...core import IGetUserIdByPhoneQuery

from amocrm_asterisk_ng.domain import IRaiseCardCommand
from .RaiseCardCommand import RaiseCardCommand

from .event_handlers import RingingEventHandler


__all__ = [
    "RaiseCardComponent",
]


class RaiseCardComponent(InitializableComponent):

    __slots__ = (
        "__amo_client",
        "__event_bus",
        "__dispatcher",
        "__get_user_id_by_phone_query",
        "__logger",
    )

    def __init__(
        self,
        amo_client: AmoCrmApiClient,
        dispatcher: IDispatcher,
        get_user_id_by_phone_query: IGetUserIdByPhoneQuery,
        logger: ILogger,
    ) -> None:
        self.__amo_client = amo_client
        self.__event_bus = event_bus
        self.__dispatcher = dispatcher
        self.__get_user_id_by_phone_query = get_user_id_by_phone_query
        self.__logger = logger

    async def initialize(self) -> None:

        self.__dispatcher.add_function(
            function_type=IRaiseCardCommand,
            function=RaiseCardCommand(
                amo_client=self.__amo_client,
                logger=self.__logger,
            )
        )

    async def deinitialize(self) -> None:
        self.__dispatcher.delete_function(
            IRaiseCardCommand,
        )
