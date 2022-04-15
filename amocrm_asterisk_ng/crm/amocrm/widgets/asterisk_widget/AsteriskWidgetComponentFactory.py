from typing import Mapping
from typing import Any
from typing import Optional

from fastapi import FastAPI
from amocrm_asterisk_ng.infrastructure import ISelectableFactory
from amocrm_asterisk_ng.infrastructure import ioc
from amocrm_asterisk_ng.infrastructure import ISetContextVarsFunction
from amocrm_asterisk_ng.infrastructure import InitializableComponent
from amocrm_asterisk_ng.infrastructure import IDispatcher
from amocrm_asterisk_ng.infrastructure import IEventBus
from amocrm_asterisk_ng.infrastructure import ILogger

from .AsteriskWidgetComponent import AsteriskWidgetComponent
from .AsteriskWidgetConfig import AsteriskWidgetConfig
from .views import WidgetView
from amocrm_asterisk_ng.infrastructure import ISetContextVarsFunction


__all__ = [
    "AsteriskWidgetComponentFactory"
]


class AsteriskWidgetComponentFactory(ISelectableFactory[InitializableComponent]):

    __slots__ = (
        "__app",
        "__dispatcher",
        "__event_bus",
        "__set_context_vars_function",
        "__logger",
    )

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

    def unique_tag(self) -> str:
        return "asterisk_widget"

    def get_instance(
        self,
        settings: Optional[Mapping[str, Any]] = None
    ) -> InitializableComponent:

        config = AsteriskWidgetConfig(**settings)

        widget_view = WidgetView(
            config=config,
            event_bus=self.__event_bus,
            set_context_vars_function=self.__set_context_vars_function,
            logger=self.__logger,
        )

        component = AsteriskWidgetComponent(
            config=config,
            app=self.__app,
            dispatcher=self.__dispatcher,
            widget_view=widget_view,
            logger=self.__logger,
        )
        return component
