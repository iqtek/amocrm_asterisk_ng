from asyncio import create_task
from typing import Optional
from asyncio import sleep
from glassio.dispatcher import IDispatcher
from glassio.initializable_components import AbstractInitializableComponent
from glassio.logger import ILogger

from amocrm_asterisk_ng.domain import IGetRecordFileUniqueIdQuery

from .CdrProviderConfig import CdrProviderConfig
from .mysql import MySqlConnectionFactoryImpl
from .query_handlers import GetRecordFileUniqueIdQuery


__all__ = [
    "CdrProviderComponent",
]


class CdrProviderComponent(AbstractInitializableComponent):

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
        super().__init__()
        self.__config = config
        self.__mysql_connection_factory = mysql_connection_factory
        self.__dispatcher = dispatcher
        self.__logger = logger

    async def _initialize(self) -> None:
        self.__dispatcher.add_function(
            function_type=IGetRecordFileUniqueIdQuery,
            function=GetRecordFileUniqueIdQuery(
                config=self.__config,
                mysql_connection_factory=self.__mysql_connection_factory,
                logger=self.__logger,
            )
        )

    async def _deinitialize(self, exception: Optional[Exception] = None) -> None:
        self.__dispatcher.delete_function(IGetRecordFileUniqueIdQuery)
