from asyncio import AbstractEventLoop
from typing import Collection
from typing import Mapping
from typing import Any

from fastapi import FastAPI
from pydantic import ValidationError

from amocrm_asterisk_ng.telephony import telephony_startup
from amocrm_asterisk_ng.crm import crm_startup
from amocrm_asterisk_ng.scenario import scenario_startup
from amocrm_asterisk_ng.scenario import IScenario
from amocrm_asterisk_ng.infrastructure import ioc
from amocrm_asterisk_ng.infrastructure import ILogger
from amocrm_asterisk_ng.infrastructure import InitializableComponent
from amocrm_asterisk_ng.infrastructure import InitializableEventBus
from amocrm_asterisk_ng.infrastructure import logger_startup
from amocrm_asterisk_ng.infrastructure import storage_startup
from amocrm_asterisk_ng.infrastructure import dispatcher_startup
from amocrm_asterisk_ng.infrastructure import event_bus_startup
from amocrm_asterisk_ng.infrastructure import Version

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

        ioc.set("listening_components", [])
        ioc.set("control_components", [])
        ioc.set("infrastructure_components", [])

        ioc.set_instance(
            key=FastAPI,
            instance=self.__app,
        )

        ioc.set_instance(
            key=AbstractEventLoop,
            instance=event_loop,
        )

        logger_startup(
            settings=config.infrastructure.logger,
        )

        storage_startup(
            settings=config.infrastructure.storage,
        )

        dispatcher_startup()

        event_bus_startup(settings={"type": "memory"})

        scenario_startup(
            scenario_name=config.scenario,
            scenario_configs_dir=config.scenario_configs_dir
        )
        crm_component = crm_startup(settings=config.crm)

        telephony_startup(settings=config.telephony)

        logger = ioc.get_instance(ILogger)
        scenario = ioc.get_instance(IScenario)

        event_bus = ioc.get_instance(InitializableEventBus)
        control_components = ioc.get("control_components") + [crm_component]
        listening_components = ioc.get("listening_components")

        integration = Integration(
            scenario=scenario,
            listening_components=listening_components,
            control_components=control_components,
            infrastructure_components=[event_bus],
            logger=logger,
        )
        return integration
