from typing import Any
from typing import Mapping
from typing import Optional

from aiomysql import Connection
from aiomysql import connect

from asterisk_ng.system.dispatcher import IDispatcher
from asterisk_ng.system.logger import ILogger

from asterisk_ng.interfaces import IGetRecordFileByUniqueIdQuery
from asterisk_ng.system.container import Key
from asterisk_ng.system.container import container
from asterisk_ng.system.plugin import IPlugin
from asterisk_ng.system.plugin import Interface
from asterisk_ng.system.plugin import PluginInterface
from asterisk_ng.system.plugin import AbstractPlugin

from .GetRecordFileUniqueIdQuery import GetRecordFileByUniqueIdQuery
from .configs import RecordsProviderPluginConfig


__all__ = ["RecordsProviderPlugin"]


class RecordsProviderPlugin(AbstractPlugin):

    __slots__ = (
        "__dispatcher",
        "__connection",
    )

    def __init__(self) -> None:
        self.__dispatcher: Optional[IDispatcher] = None
        self.__connection: Optional[Connection] = None

    @property
    def interface(self) -> PluginInterface:
        return PluginInterface(
            imported=Interface(
                container=[
                    Key(ILogger)
                ],
            ),
            exported=Interface(
                dispatcher=[IGetRecordFileByUniqueIdQuery],
            )
        )

    async def upload(self, settings: Mapping[str, Any]) -> None:

        self.__dispatcher = container.resolve(Key(IDispatcher))
        logger = container.resolve(Key(ILogger))

        config = RecordsProviderPluginConfig(**settings)

        self.__connection = await connect(
            user=config.mysql.user,
            password=config.mysql.password,
            host=config.mysql.host,
            port=config.mysql.port,
            db=config.mysql.database,
        )

        self.__dispatcher.add_function(
            IGetRecordFileByUniqueIdQuery,
            GetRecordFileByUniqueIdQuery(
                config=config,
                connection=self.__connection,
                logger=logger
            )
        )

    async def unload(self) -> None:
        self.__dispatcher.delete_function(IGetRecordFileByUniqueIdQuery)
        self.__connection.close()
