from typing import Any
from typing import Mapping
from typing import Optional
from fastapi import FastAPI

from amocrm_asterisk_ng.infrastructure import IDispatcher
from amocrm_asterisk_ng.infrastructure import IEventBus
from amocrm_asterisk_ng.infrastructure import IKeyValueStorageFactory
from amocrm_asterisk_ng.infrastructure import ILogger
from amocrm_asterisk_ng.infrastructure import InitializableComponent
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
        "__storage_factory",
        "__logger",
    )

    def __init__(
        self,
        app: FastAPI,
        event_bus: IEventBus,
        dispatcher: IDispatcher,
        storage_factory: IKeyValueStorageFactory,
        logger: ILogger,
    ) -> None:
        self.__app = app
        self.__dispatcher = dispatcher
        self.__event_bus = event_bus
        self.__storage_factory = storage_factory
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
