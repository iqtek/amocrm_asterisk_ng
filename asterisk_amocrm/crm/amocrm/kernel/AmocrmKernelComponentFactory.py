from typing import Mapping, Any
from asterisk_amocrm.infrastructure import (
    IComponent,
    IEventBus,
    IDispatcher,
    IKeyValueStorage,
    ILogger,
)
from fastapi import FastAPI
from .calls import CallManagerComponent
from .AmocrmKernelComponent import AmocrmKernelComponent
from amo_crm_api_client import create_amo_crm_api_client, AmoCrmApiClientConfig
from .raise_card import RaiseCardComponent
__all__ = [
    "AmocrmKernelComponentFactory"
]


class AmocrmKernelComponentFactory:

    def __init__(
        self,
        app: FastAPI,
        event_bus: IEventBus,
        dispatcher: IDispatcher,
        storage: IKeyValueStorage,
        logger: ILogger,
    ) -> None:
        self.__app = app
        self.__dispatcher = dispatcher
        self.__event_bus = event_bus
        self.__storage = storage
        self.__logger = logger

    def get_instance(self, settings: Mapping[str, Any]) -> IComponent:

        config = AmoCrmApiClientConfig(
            integration_id=settings["integration"]["integration_id"],
            secret_key=settings["integration"]["secret_key"],
            auth_code=settings["integration"]["auth_code"],
            redirect_uri=settings["integration"]["redirect_uri"],
            base_url=settings["integration"]["base_url"],
        )

        amo_client = create_amo_crm_api_client(
            config=config,
            key_value_storage=self.__storage,
        )

        call_manager_component = CallManagerComponent(
            settings=settings["call_logging"],
            app=self.__app,
            amo_client=amo_client,
            dispatcher=self.__dispatcher,
            event_bus=self.__event_bus,
            logger=self.__logger,
        )

        raise_card_component = RaiseCardComponent(
            amo_client=amo_client,
            dispatcher=self.__dispatcher,
            event_bus=self.__event_bus,
            logger=self.__logger,
        )

        amocrm_kernel_component = AmocrmKernelComponent(
            dispatcher=self.__dispatcher,
            amo_client=amo_client,
            raise_card_component=raise_card_component,
            call_manager_component=call_manager_component,

        )

        return amocrm_kernel_component
