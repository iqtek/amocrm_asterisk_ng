from typing import Any
from typing import Mapping
from typing import Optional

from fastapi import FastAPI
from glassio.dispatcher import IDispatcher
from glassio.initializable_components import InitializableComponent
from glassio.logger import ILogger

from amocrm_asterisk_ng.domain import IOriginationRequestCommand
from amocrm_asterisk_ng.infrastructure import ISelectableFactory
from .AsteriskWidgetComponent import AsteriskWidgetComponent
from .AsteriskWidgetConfig import AsteriskWidgetConfig
from .WidgetView import WidgetView


__all__ = [
    "AsteriskWidgetComponentFactory"
]


class AsteriskWidgetComponentFactory(ISelectableFactory[InitializableComponent]):

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

    def unique_tag(self) -> str:
        return "asterisk_widget"

    def get_instance(
        self,
        settings: Optional[Mapping[str, Any]] = None
    ) -> InitializableComponent:

        config = AsteriskWidgetConfig(**settings)

        widget_view = WidgetView(
            config=config,
            origination_request_command=self.__dispatcher.get_function(IOriginationRequestCommand),
            logger=self.__logger,
        )

        component = AsteriskWidgetComponent(
            config=config,
            app=self.__app,
            dispatcher=self.__dispatcher,
            widget_view=widget_view,
        )
        return component
