from typing import Any
from typing import Mapping

from amo_crm_api_client import AmoCrmApiClient
from fastapi import FastAPI

from amocrm_asterisk_ng.infrastructure import IDispatcher
from amocrm_asterisk_ng.infrastructure import IEventBus
from amocrm_asterisk_ng.infrastructure import ILogger
from amocrm_asterisk_ng.infrastructure import InitializableComponent

from .call_records import call_records_startup
from .calls_logging import CallLoggingConfig
from .calls_logging.commands_handlers import AddCallToAnalyticsCommand
from .calls_logging.commands_handlers import AddCallToUnsortedCommand
from .calls_logging.commands_handlers import IAddCallToAnalyticsCommand
from .calls_logging.commands_handlers import IAddCallToUnsortedCommand

from .calls_logging.event_handlers import CdrDetectionEventHandler
from ...core import IGetUserIdByPhoneQuery


__all__ = [
    "CallManagerComponent",
]


class CallManagerComponent(InitializableComponent):

    __slots__ = (
        "__config",
        "__app",
        "__amo_client",
        "__event_bus",
        "__dispatcher",
        "__get_user_id_by_phone_query",
        "__logger",
    )

    def __init__(
        self,
        settings: Mapping[str, Any],
        app: FastAPI,
        amo_client: AmoCrmApiClient,
        event_bus: IEventBus,
        dispatcher: IDispatcher,
        get_user_id_by_phone_query: IGetUserIdByPhoneQuery,
        logger: ILogger,
    ) -> None:
        self.__app = app
        self.__amo_client = amo_client
        self.__event_bus = event_bus
        self.__dispatcher = dispatcher
        self.__get_user_id_by_phone_query = get_user_id_by_phone_query
        self.__logger = logger
        self.__config = CallLoggingConfig(**settings)

    async def initialize(self) -> None:
        call_records_startup(
            settings={'tmp_directory': self.__config.tmp_directory},
            endpoint_format_string="/amocrm/cdr/{unique_id}.mp3",
            app=self.__app,
            dispatcher=self.__dispatcher,
            logger=self.__logger,
        )

        self.__dispatcher.add_function(
            function_type=IAddCallToAnalyticsCommand,
            function=AddCallToAnalyticsCommand(
                amo_client=self.__amo_client,
                logger=self.__logger,
            )
        )
        self.__dispatcher.add_function(
            function_type=IAddCallToUnsortedCommand,
            function=AddCallToUnsortedCommand(
                amo_client=self.__amo_client,
                logger=self.__logger,
            )
        )

        add_call_to_analytics_command = self.__dispatcher.get_function(IAddCallToAnalyticsCommand)
        add_call_to_unsorted_command = self.__dispatcher.get_function(IAddCallToUnsortedCommand)

        await self.__event_bus.attach_event_handler(
            CdrDetectionEventHandler(
                config=self.__config,
                cdr_endpoint_format_string="/amocrm/cdr/{}.mp3",
                add_call_to_analytics_command=add_call_to_analytics_command,
                add_call_to_unsorted_command=add_call_to_unsorted_command,
                get_user_id_by_phone_query=self.__get_user_id_by_phone_query,
                logger=self.__logger,
            )
        )

    async def deinitialize(self) -> None:
        await self.__event_bus.detach_event_handler(
            CdrDetectionEventHandler,
        )

        self.__dispatcher.delete_function(
            IAddCallToAnalyticsCommand,
        )

        self.__dispatcher.delete_function(
            IAddCallToUnsortedCommand,
        )
