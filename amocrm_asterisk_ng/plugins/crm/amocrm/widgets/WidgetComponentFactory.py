from typing import Any
from typing import Mapping
from typing import Optional

from fastapi import FastAPI

from glassio.dispatcher import IDispatcher
from glassio.initializable_components import InitializableComponent
from glassio.logger import ILogger
from glassio.mixins import IFactory

from amocrm_asterisk_ng.infrastructure import SelectedComponentConfig
from amocrm_asterisk_ng.infrastructure import SelectorImpl

from .asterisk_widget import AsteriskWidgetComponentFactory


__all__ = [
    "WidgetComponentFactory",
]


class WidgetComponentFactory(IFactory[InitializableComponent]):

    __slots__ = (
        "__app",
        "__dispatcher",
        "__logger",
    )

    def __init__(
        self,
        app: FastAPI,
        dispatcher: IDispatcher,
        logger: ILogger,
    ) -> None:
        self.__app = app
        self.__dispatcher = dispatcher
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
