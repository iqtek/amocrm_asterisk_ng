from typing import Any
from typing import Mapping
from typing import Optional

from amo_crm_api_client import AmoCrmApiClientConfig
from amo_crm_api_client import create_amo_crm_api_client
from fastapi import FastAPI

from asterisk_amocrm.infrastructure import IDispatcher
from asterisk_amocrm.infrastructure import IEventBus
from asterisk_amocrm.infrastructure import IFactory
from asterisk_amocrm.infrastructure import IKeyValueStorage
from asterisk_amocrm.infrastructure import ILogger
from asterisk_amocrm.infrastructure import InitializableComponent

from .AmocrmKernelComponent import AmocrmKernelComponent
from .AmocrmKernelComponentConfig import AmocrmKernelComponentConfig
from .calls import CallManagerComponent
from .raise_card import RaiseCardComponent

from ..core import IGetUserEmailByPhoneQuery
from ..core import IGetUserIdByPhoneQuery


__all__ = [
    "AmocrmKernelComponentFactory"
]


class AmocrmKernelComponentFactory(IFactory[InitializableComponent]):

    __slots__ = (
        "__app",
        "__dispatcher",
        "__event_bus",
        "__storage",
        "__logger",
    )

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

    def get_instance(
        self,
        settings: Optional[Mapping[str, Any]] = None,
    ) -> InitializableComponent:

        settings = settings or {}
        component_config = AmocrmKernelComponentConfig(**settings)

        amo_client_config = AmoCrmApiClientConfig(**component_config.integration)

        amo_client = create_amo_crm_api_client(
            config=amo_client_config,
            key_value_storage=self.__storage,
        )

        get_user_id_by_phone_query = self.__dispatcher.get_function(IGetUserIdByPhoneQuery)

        call_manager_component = CallManagerComponent(
            settings=component_config.call_logging,
            app=self.__app,
            amo_client=amo_client,
            dispatcher=self.__dispatcher,
            get_user_id_by_phone_query=get_user_id_by_phone_query,
            event_bus=self.__event_bus,
            logger=self.__logger,
        )

        raise_card_component = RaiseCardComponent(
            amo_client=amo_client,
            dispatcher=self.__dispatcher,
            event_bus=self.__event_bus,
            get_user_id_by_phone_query=get_user_id_by_phone_query,
            logger=self.__logger,
        )

        get_user_email_by_phone_query = self.__dispatcher.get_function(IGetUserEmailByPhoneQuery)

        amocrm_kernel_component = AmocrmKernelComponent(
            dispatcher=self.__dispatcher,
            amo_client=amo_client,
            raise_card_component=raise_card_component,
            call_manager_component=call_manager_component,
            get_user_id_by_phone_query=get_user_id_by_phone_query,
            get_user_email_by_phone_query=get_user_email_by_phone_query,
        )

        return amocrm_kernel_component
