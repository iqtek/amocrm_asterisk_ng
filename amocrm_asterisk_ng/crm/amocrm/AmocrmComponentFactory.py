from typing import Mapping, Any, Optional
from amocrm_asterisk_ng.infrastructure import ISelectableFactory
from amocrm_asterisk_ng.infrastructure import (
    InitializableComponent,
    IEventBus,
    IDispatcher,
    ILogger,
    IKeyValueStorageFactory,
    ISetContextVarsFunction,
)
from fastapi import FastAPI
from .kernel import AmocrmKernelComponentFactory
from .widgets import WidgetComponentFactory
from .AmocrmComponent import AmocrmComponent
from .AmocrmComponentConfig import AmocrmComponentConfig


__all__ = [
    "AmocrmComponentFactory"
]


class AmocrmComponentFactory(ISelectableFactory):

    __slots__ = (
        "__app",
        "__dispatcher",
        "__event_bus",
        "__storage_factory",
        "__set_context_vars_function",
        "__logger",
    )

    def __init__(
        self,
        app: FastAPI,
        event_bus: IEventBus,
        dispatcher: IDispatcher,
        storage_factory: IKeyValueStorageFactory,
        set_context_vars_function: ISetContextVarsFunction,
        logger: ILogger,
    ) -> None:
        self.__app = app
        self.__dispatcher = dispatcher
        self.__event_bus = event_bus
        self.__storage_factory = storage_factory
        self.__set_context_vars_function = set_context_vars_function
        self.__logger = logger

    def unique_tag(self) -> str:
        return "amocrm"

    def get_instance(
        self,
        settings: Optional[Mapping[str, Any]] = None
    ) -> InitializableComponent:
        config = AmocrmComponentConfig(**settings)
        storage = self.__storage_factory.get_instance(
            prefix=config.storage_prefix,
        )
        widget_component_factory = WidgetComponentFactory(
            app=self.__app,
            event_bus=self.__event_bus,
            dispatcher=self.__dispatcher,
            set_context_vars_function=self.__set_context_vars_function,
            logger=self.__logger,
        )

        widget_component = widget_component_factory.get_instance(
            settings=config.widget,
        )

        amocrm_kernel_factory = AmocrmKernelComponentFactory(
            app=self.__app,
            event_bus=self.__event_bus,
            dispatcher=self.__dispatcher,
            storage=storage,
            logger=self.__logger,
        )
        amocrm_kernel_component = amocrm_kernel_factory.get_instance(
            settings=config.kernel,
        )

        amocrm_component = AmocrmComponent(
            amocrm_kernel_component=amocrm_kernel_component,
            widget_component=widget_component,
        )

        return amocrm_component
