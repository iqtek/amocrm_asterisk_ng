from typing import Optional

from amocrm_api_client import AmoCrmApiClient
from glassio.dispatcher import IDispatcher
from glassio.initializable_components import AbstractInitializableComponent
from glassio.logger import ILogger

from amocrm_asterisk_ng.domain import IRaiseCardCommand
from .RaiseCardCommand import RaiseCardCommand


__all__ = [
    "RaiseCardComponent",
]


class RaiseCardComponent(AbstractInitializableComponent):

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
        super().__init__()
        self.__amo_client = amo_client
        self.__dispatcher = dispatcher
        self.__logger = logger

    async def _initialize(self) -> None:

        self.__dispatcher.add_function(
            function_type=IRaiseCardCommand,
            function=RaiseCardCommand(
                amo_client=self.__amo_client,
                logger=self.__logger,
            )
        )

    async def _deinitialize(self, exception: Optional[Exception] = None) -> None:
        self.__dispatcher.delete_function(
            IRaiseCardCommand,
        )
