from asyncio import AbstractEventLoop
from typing import Any
from typing import Mapping

from fastapi import FastAPI
from pydantic import ValidationError

from glassio.logger import ILogger
from glassio.event_bus import InitializableEventBus
from amocrm_asterisk_ng.infrastructure import ioc
from amocrm_asterisk_ng.scenario import IScenario

from .bootstrap import bootstrap
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

        ioc.set_instance(IntegrationConfig, config)
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

        bootstrap()

        logger = ioc.get_instance(ILogger)
        scenario = ioc.get_instance(IScenario)

        control_components = ioc.get("control_components")
        listening_components = ioc.get("listening_components")
        infrastructure_components = ioc.get("infrastructure_components")

        integration = Integration(
            scenario=scenario,
            listening_components=listening_components,
            control_components=control_components,
            infrastructure_components=infrastructure_components,
            logger=logger,
        )
        return integration
