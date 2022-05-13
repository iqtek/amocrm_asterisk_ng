from typing import Mapping
from typing import Optional
from typing import Any

from fastapi import FastAPI

from amocrm_asterisk_ng.infrastructure import SelectorImpl
from amocrm_asterisk_ng.infrastructure import SelectedComponentConfig
from glassio.initializable_components import InitializableComponent
from glassio.event_bus import IEventBus
from amocrm_asterisk_ng.infrastructure import IFactory
from glassio.dispatcher import IDispatcher
from glassio.logger import ILogger

from .asterisk_widget import AsteriskWidgetComponentFactory


__all__ = [
    "WidgetComponentFactory",
]


class WidgetComponentFactory(IFactory[InitializableComponent]):

    __slots__ = (
        "__app",
        "__dispatcher",
        "__event_bus",
        "__logger",
    )

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

    def get_instance(
        self,
        settings: Optional[Mapping[str, Any]] = None
    ) -> InitializableComponent:

        settings = settings or {}
        startup_config = SelectedComponentConfig(**settings)

        selector = SelectorImpl()

        asterisk_widget_factory = AsteriskWidgetComponentFactory(
            app=self.__app,
            dispatcher=self.__dispatcher,
            logger=self.__logger,
        )

        selector.add_item(asterisk_widget_factory)

        factory = selector.get_item(unique_tag=startup_config.type)

        widget_component = factory.get_instance(
            settings=startup_config.settings,
        )

        return widget_component
