from asyncio import AbstractEventLoop
from typing import Any, Mapping

from asterisk_amocrm.infrastructure import (IComponent, IDispatcher, ILogger)
from .CdrProviderComponent import CdrProviderComponent
from .CdrProviderConfig import CdrProviderConfig
from .mysql import MySqlConnectionFactoryImpl


__all__ = [
    "CdrProviderComponentFactory",
]


class CdrProviderComponentFactory:

    def __init__(
        self,
        dispatcher: IDispatcher,
        event_loop: AbstractEventLoop,
        logger: ILogger,
    ) -> None:
        self.__dispatcher = dispatcher
        self.__event_loop = event_loop
        self.__logger = logger

    def get_instance(self, settings: Mapping[str, Any]) -> IComponent:

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
