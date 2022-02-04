from typing import (
    Mapping,
    Any,
)

from fastapi import FastAPI

from asterisk_amocrm.infrastructure import (
    IComponent,
    IEventBus,
    IDispatcher,
    ILogger,
    FactoryStoreImpl,
)
from .asterisk_widget import AsteriskWidgetComponentFactory


__all__ = [
    "WidgetComponentFactory",
]


class WidgetComponentFactory:

    def __init__(
        self,
        app: FastAPI,
        event_bus: IEventBus,
        dispatcher: IDispatcher,
        logger: ILogger,
    ) -> None:
        self.__app = app
        self.__dispatcher = dispatcher
        self.__event_bus = event_bus
        self.__logger = logger

    def get_instance(self, settings: Mapping[str, Any]) -> IComponent:

        widget_type = settings["type"]
        widget_settings = settings["settings"]

        factory_store = FactoryStoreImpl()

        asterisk_widget_factory = AsteriskWidgetComponentFactory(
            app=self.__app,
            event_bus=self.__event_bus,
            dispatcher=self.__dispatcher,
            logger=self.__logger,
        )
        factory_store.register_factory(asterisk_widget_factory)

        widget_component = factory_store.get_instance(
            type=widget_type,
            settings=widget_settings,
        )

        return widget_component
