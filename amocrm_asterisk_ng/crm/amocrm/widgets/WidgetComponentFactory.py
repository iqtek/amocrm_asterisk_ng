from typing import Mapping
from typing import Optional
from typing import Any

from fastapi import FastAPI

from amocrm_asterisk_ng.infrastructure import SelectorImpl
from amocrm_asterisk_ng.infrastructure import SelectedComponentConfig
from amocrm_asterisk_ng.infrastructure import ISetContextVarsFunction
from amocrm_asterisk_ng.infrastructure import InitializableComponent
from amocrm_asterisk_ng.infrastructure import IEventBus
from amocrm_asterisk_ng.infrastructure import IFactory
from amocrm_asterisk_ng.infrastructure import IDispatcher
from amocrm_asterisk_ng.infrastructure import ILogger

from .asterisk_widget import AsteriskWidgetComponentFactory


__all__ = [
    "WidgetComponentFactory",
]


class WidgetComponentFactory(IFactory[InitializableComponent]):

    def __init__(
        self,
        app: FastAPI,
        event_bus: IEventBus,
        dispatcher: IDispatcher,
        set_context_vars_function: ISetContextVarsFunction,
        logger: ILogger,
    ) -> None:
        self.__app = app
        self.__dispatcher = dispatcher
        self.__event_bus = event_bus
        self.__set_context_vars_function = set_context_vars_function
        self.__logger = logger

    def get_instance(
        self,
        settings: Optional[Mapping[str, Any]] = None
    ) -> InitializableComponent:

        settings = settings or {}
        startup_config = SelectedComponentConfig(**settings)

        selector = SelectorImpl()

        asterisk_widget_factory = AsteriskWidgetComponentFactory(
            app=self.__app,
            event_bus=self.__event_bus,
            dispatcher=self.__dispatcher,
            set_context_vars_function=self.__set_context_vars_function,
            logger=self.__logger,
        )

        selector.add_item(asterisk_widget_factory)

        factory = selector.get_item(unique_tag=startup_config.type)

        widget_component = factory.get_instance(
            settings=startup_config.settings,
        )

        return widget_component
