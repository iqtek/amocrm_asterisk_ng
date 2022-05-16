from typing import Any
from typing import Mapping
from typing import Optional

from fastapi import FastAPI
from glassio.dispatcher import IDispatcher
from glassio.event_bus import IEventBus
from glassio.initializable_components import InitializableComponent
from glassio.logger import ILogger

from amocrm_asterisk_ng.infrastructure import ISelectableFactory
from .AmocrmComponent import AmocrmComponent
from .AmocrmComponentConfig import AmocrmComponentConfig
from .kernel import AmocrmKernelComponentFactory
from .widgets import WidgetComponentFactory


__all__ = [
    "AmocrmComponentFactory"
]


class AmocrmComponentFactory(ISelectableFactory):

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

    def unique_tag(self) -> str:
        return "amocrm"

    def get_instance(
        self,
        settings: Optional[Mapping[str, Any]] = None
    ) -> InitializableComponent:
        config = AmocrmComponentConfig(**settings)

        widget_component_factory = WidgetComponentFactory(
            app=self.__app,
            dispatcher=self.__dispatcher,
            logger=self.__logger,
        )

        widget_component = widget_component_factory.get_instance(
            settings=config.widget,
        )

        amocrm_kernel_factory = AmocrmKernelComponentFactory(
            app=self.__app,
            dispatcher=self.__dispatcher,
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
