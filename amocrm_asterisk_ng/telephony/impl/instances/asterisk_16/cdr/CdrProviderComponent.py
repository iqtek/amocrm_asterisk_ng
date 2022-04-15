import os

from amocrm_asterisk_ng.domain import IGetCdrByUniqueIdQuery
from amocrm_asterisk_ng.infrastructure import IDispatcher
from amocrm_asterisk_ng.infrastructure import ILogger
from amocrm_asterisk_ng.infrastructure import InitializableComponent

from .CdrProviderConfig import CdrProviderConfig
from .mysql import MySqlConnectionFactoryImpl
from .query_handlers import GetCdrByUniqueIdQuery


__all__ = [
    "CdrProviderComponent",
]


class CdrProviderComponent(InitializableComponent):

    __slots__ = (
        "__config",
        "__mysql_connection_factory",
        "__dispatcher",
        "__logger",
    )

    def __init__(
        self,
        config: CdrProviderConfig,
        mysql_connection_factory: MySqlConnectionFactoryImpl,
        dispatcher: IDispatcher,
        logger: ILogger,
    ) -> None:
        self.__config = config
        self.__mysql_connection_factory = mysql_connection_factory
        self.__dispatcher = dispatcher
        self.__logger = logger

    async def initialize(self) -> None:
        self.__dispatcher.add_function(
            function_type=IGetCdrByUniqueIdQuery,
            function=GetCdrByUniqueIdQuery(
                config=self.__config,
                mysql_connection_factory=self.__mysql_connection_factory,
                logger=self.__logger,
            )
        )

    async def deinitialize(self) -> None:

        self.__dispatcher.delete_function(
            function_type=IGetCdrByUniqueIdQuery,
        )
