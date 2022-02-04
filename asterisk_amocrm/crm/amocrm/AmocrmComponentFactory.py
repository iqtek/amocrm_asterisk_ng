from typing import Mapping, Any
from asterisk_amocrm.infrastructure import (
    IComponent,
    IFactory,
    IEventBus,
    IDispatcher,
    ILogger,
    IKeyValueStorage,
)
from fastapi import FastAPI
from .kernel import AmocrmKernelComponentFactory
from .widgets import WidgetComponentFactory
from .AmocrmComponent import AmocrmComponent


__all__ = [
    "AmocrmComponentFactory"
]


class AmocrmComponentFactory(IFactory):

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

    @classmethod
    def type(cls) -> str:
        return "amocrm"

    def get_instance(self, settings: Mapping[str, Any]) -> IComponent:
        widget_component_factory = WidgetComponentFactory(
            app=self.__app,
            event_bus=self.__event_bus,
            dispatcher=self.__dispatcher,
            logger=self.__logger,
        )

        widget_component = widget_component_factory.get_instance(
            settings=settings["widget"],
        )

        amocrm_kernel_factory = AmocrmKernelComponentFactory(
            app=self.__app,
            event_bus=self.__event_bus,
            dispatcher=self.__dispatcher,
            storage=self.__storage,
            logger=self.__logger,
        )
        amocrm_kernel_component = amocrm_kernel_factory.get_instance(
            settings["kernel"],
        )

        amocrm_component = AmocrmComponent(
            amocrm_kernel_component=amocrm_kernel_component,
            widget_component=widget_component,
        )

        return amocrm_component
