from asyncio import AbstractEventLoop
from typing import Collection
from typing import Mapping
from typing import Any

from fastapi import FastAPI
from pydantic import ValidationError

from asterisk_amocrm.telephony import telephony_startup
from asterisk_amocrm.crm import crm_startup
from asterisk_amocrm.infrastructure import ioc
from asterisk_amocrm.infrastructure import ILogger
from asterisk_amocrm.infrastructure import context_vars_startup
from asterisk_amocrm.infrastructure import InitializableComponent
from asterisk_amocrm.infrastructure import InitializableMessageBus
from asterisk_amocrm.infrastructure import InitializableEventBus
from asterisk_amocrm.infrastructure import logger_startup
from asterisk_amocrm.infrastructure import storage_startup
from asterisk_amocrm.infrastructure import dispatcher_startup
from asterisk_amocrm.infrastructure import event_bus_startup
from asterisk_amocrm.infrastructure import message_bus_startup
from asterisk_amocrm.infrastructure import get_current_version_func_startup
from asterisk_amocrm.infrastructure import Version

from .Integration import Integration
from .IntegrationConfig import IntegrationConfig


__all__ = [
    "IntegrationFactory",
]


class IntegrationFactory:

    __slots__ = (
        "__app",
        "__current_app_version",
    )

    def __init__(
        self,
        app: FastAPI,
        current_app_version: str,
    ) -> None:
        self.__app = app
        self.__current_app_version = current_app_version

    def get_instance(
        self,
        settings: Mapping[str, Any],
        event_loop: AbstractEventLoop,
    ) -> Integration:

        try:
            config = IntegrationConfig(**settings)
        except ValidationError as e:
            raise Exception(
                "Make sure you have executed the "
                f"configuration file correctly. {e}"
            )

        ioc.set_instance(
            key=FastAPI,
            instance=self.__app,
        )
        ioc.set_instance(
            key=AbstractEventLoop,
            instance=event_loop,
        )

        get_current_version_func_startup()

        logger_startup(
            settings=config.infrastructure.logger,
        )

        context_vars_startup()

        storage_startup(
            settings=config.infrastructure.storage,
        )

        dispatcher_startup()

        message_bus_startup(
            settings=config.infrastructure.message_bus,
        )

        event_bus_startup(
            settings=config.infrastructure.event_bus,
        )

        crm_component = crm_startup(settings=config.crm)

        telephony_component = telephony_startup(settings=config.telephony)

        components: Collection[InitializableComponent] = [
            ioc.get_instance(InitializableMessageBus),
            ioc.get_instance(InitializableEventBus),
            crm_component,
            telephony_component,
        ]

        logger = ioc.get_instance(ILogger)

        integration = Integration(
            components=components,
            logger=logger,
        )
        return integration
