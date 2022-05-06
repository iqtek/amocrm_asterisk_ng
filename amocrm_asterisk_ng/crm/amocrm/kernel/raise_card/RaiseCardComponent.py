from amocrm_api_client import AmoCrmApiClient

from amocrm_asterisk_ng.domain import IRaiseCardCommand
from amocrm_asterisk_ng.infrastructure import IDispatcher
from amocrm_asterisk_ng.infrastructure import ILogger
from amocrm_asterisk_ng.infrastructure import InitializableComponent

from .RaiseCardCommand import RaiseCardCommand


__all__ = [
    "RaiseCardComponent",
]


class RaiseCardComponent(InitializableComponent):

    __slots__ = (
        "__amo_client",
        "__event_bus",
        "__dispatcher",
        "__logger",
    )

    def __init__(
        self,
        amo_client: AmoCrmApiClient,
        dispatcher: IDispatcher,
        logger: ILogger,
    ) -> None:
        self.__amo_client = amo_client
        self.__dispatcher = dispatcher
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
