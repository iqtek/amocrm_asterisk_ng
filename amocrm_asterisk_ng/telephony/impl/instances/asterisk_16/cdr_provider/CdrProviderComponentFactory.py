from asyncio import AbstractEventLoop
from typing import Any
from typing import Mapping
from typing import Optional

from glassio.dispatcher import IDispatcher
from glassio.mixins import IFactory
from glassio.logger import ILogger
from glassio.initializable_components import AbstractInitializableComponent
from glassio.initializable_components import InitializableComponent

from .CdrProviderComponent import CdrProviderComponent
from .CdrProviderConfig import CdrProviderConfig
from .mysql import MySqlConnectionFactoryImpl


__all__ = [
    "CdrProviderComponentFactory",
]


class CdrProviderComponentFactory(IFactory[InitializableComponent]):

    __slots__ = (
        "__dispatcher",
        "__event_loop",
        "__logger",
    )

    def __init__(
        self,
        dispatcher: IDispatcher,
        event_loop: AbstractEventLoop,
        logger: ILogger,
    ) -> None:
        self.__dispatcher = dispatcher
        self.__event_loop = event_loop
        self.__logger = logger

    def get_instance(
        self,
        settings: Optional[Mapping[str, Any]] = None,
    ) -> InitializableComponent:
        settings = settings or {}

        config = CdrProviderConfig(**settings)

        mysql_connection_factory = MySqlConnectionFactoryImpl(
            event_loop=self.__event_loop,
        )

        component = CdrProviderComponent(
            config=config,
            mysql_connection_factory=mysql_connection_factory,
            dispatcher=self.__dispatcher,
            logger=self.__logger,
        )

        return component
