from typing import Any
from typing import Mapping
from typing import Optional

from amocrm_api_client import AmoCrmApiClient
from fastapi import FastAPI
from glassio.dispatcher import IDispatcher
from glassio.initializable_components import AbstractInitializableComponent
from glassio.logger import ILogger

from amocrm_asterisk_ng.domain import IAddCallToAnalyticsCommand
from amocrm_asterisk_ng.domain import IAddCallToUnsortedCommand
from .call_records import call_records_startup
from .calls_logging import AddCallToAnalyticsCommand
from .calls_logging import AddCallToUnsortedCommand
from .calls_logging import IMakeLinkFunction
from .calls_logging import MakeLinkFunctionImpl


__all__ = [
    "CallManagerComponent",
]


class CallManagerComponent(AbstractInitializableComponent):

    __slots__ = (
        "__settings",
        "__app",
        "__amo_client",
        "__event_bus",
        "__dispatcher",
        "__logger",
    )

    def __init__(
        self,
        settings: Mapping[str, Any],
        app: FastAPI,
        amo_client: AmoCrmApiClient,
        dispatcher: IDispatcher,
        logger: ILogger,
    ) -> None:
        super().__init__()
        self.__app = app
        self.__settings = settings
        self.__amo_client = amo_client
        self.__dispatcher = dispatcher
        self.__logger = logger

    async def _initialize(self) -> None:
        call_records_startup(
            settings=self.__settings,
            app=self.__app,
            dispatcher=self.__dispatcher,
            logger=self.__logger,
        )

        self.__dispatcher.add_function(
            function_type=IMakeLinkFunction,
            function=MakeLinkFunctionImpl(
                self.__settings["base_url"],
            ),
        )

        self.__dispatcher.add_function(
            function_type=IAddCallToAnalyticsCommand,
            function=AddCallToAnalyticsCommand(
                amo_client=self.__amo_client,
                make_link_function=self.__dispatcher.get_function(IMakeLinkFunction),
                logger=self.__logger,
            )
        )

        self.__dispatcher.add_function(
            function_type=IAddCallToUnsortedCommand,
            function=AddCallToUnsortedCommand(
                amo_client=self.__amo_client,
                make_link_function=self.__dispatcher.get_function(IMakeLinkFunction),
                logger=self.__logger,
            )
        )

    async def _deinitialize(self, exception: Optional[Exception] = None) -> None:

        self.__dispatcher.delete_function(
            IAddCallToAnalyticsCommand,
        )

        self.__dispatcher.delete_function(
            IAddCallToUnsortedCommand,
        )

        self.__dispatcher.delete_function(
            function_type=IMakeLinkFunction,
        )
