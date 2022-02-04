from typing import Mapping, Any
from fastapi import FastAPI
from asterisk_amocrm.infrastructure import (
    IComponent,
    IDispatcher,
    IEventBus,
    ILogger,
)
from amo_crm_api_client import AmoCrmApiClient
from .call_records import call_records_startup
from .calls_logging.event_handlers import CdrDetectionEventHandler
from .calls_logging.commands_handlers import (
    IAddCallToAnalyticsCH,
    AddCallToAnalyticsCH,
    IAddCallToUnsortedCH,
    AddCallToUnsortedCH,
)
from .calls_logging import CallLoggingConfig


__all__ = [
    "CallManagerComponent",
]


class CallManagerComponent(IComponent):

    def __init__(
        self,
        settings: Mapping[str, Any],
        app: FastAPI,
        amo_client: AmoCrmApiClient,
        event_bus: IEventBus,
        dispatcher: IDispatcher,
        logger: ILogger,
    ) -> None:
        self.__app = app
        self.__amo_client = amo_client
        self.__event_bus = event_bus
        self.__dispatcher = dispatcher
        self.__logger = logger
        self.__config = CallLoggingConfig(**settings)

    async def initialize(self) -> None:
        call_records_startup(
            app=self.__app,
            dispatcher=self.__dispatcher,
            logger=self.__logger,
        )

        await self.__dispatcher.attach_command_handler(
            IAddCallToAnalyticsCH,
            AddCallToAnalyticsCH(
                amo_client=self.__amo_client,
                logger=self.__logger,
            )
        )
        await self.__dispatcher.attach_command_handler(
            IAddCallToUnsortedCH,
            AddCallToUnsortedCH(
                amo_client=self.__amo_client,
                logger=self.__logger,
            )
        )

        await self.__event_bus.attach_event_handler(
            CdrDetectionEventHandler(
                config=self.__config,
                dispatcher=self.__dispatcher,
                logger=self.__logger,
            )
        )

    async def deinitialize(self) -> None:
        await self.__event_bus.detach_event_handler(
            CdrDetectionEventHandler,
        )

        await self.__dispatcher.detach_command_handler(
            AddCallToAnalyticsCH,
        )

        await self.__dispatcher.detach_command_handler(
            AddCallToUnsortedCH,
        )
