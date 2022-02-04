from asterisk_amocrm.domains import IGetCdrByUniqueIdQH
from asterisk_amocrm.infrastructure import IComponent, IDispatcher, ILogger
from .CdrProviderConfig import CdrProviderConfig
from .mysql import MySqlConnectionFactoryImpl
from .query_handlers import GetCdrByUniqueIdQH
from asterisk_amocrm.domains import IGetCdrByUniqueIdQH


__all__ = [
    "CdrProviderComponent",
]


class CdrProviderComponent(IComponent):

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

        await self.__dispatcher.attach_query_handler(
            IGetCdrByUniqueIdQH,
            GetCdrByUniqueIdQH(
                config=self.__config,
                mysql_connection_factory=self.__mysql_connection_factory,
                logger=self.__logger,
            )
        )

    async def deinitialize(self) -> None:

        await self.__dispatcher.detach_query_handler(
            GetCdrByUniqueIdQH,
        )
