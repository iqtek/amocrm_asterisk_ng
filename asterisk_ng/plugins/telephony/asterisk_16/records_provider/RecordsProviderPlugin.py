from typing import Any
from typing import Mapping
from typing import Optional

from aiomysql import Connection
from aiomysql import connect
from aiomysql import InterfaceError

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
        "__config",
    )

    def __init__(self) -> None:
        self.__dispatcher: Optional[IDispatcher] = None
        self.__config: Optional[RecordsProviderPluginConfig] = None

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

    async def __get_connection(self) -> Connection:
        return await connect(
            user=self.__config.mysql.user,
            password=self.__config.mysql.password,
            host=self.__config.mysql.host,
            port=self.__config.mysql.port,
            db=self.__config.mysql.database,
        )

    async def upload(self, settings: Mapping[str, Any]) -> None:

        self.__dispatcher = container.resolve(Key(IDispatcher))
        logger = container.resolve(Key(ILogger))

        self.__config = RecordsProviderPluginConfig(**settings)

        self.__dispatcher.add_function(
            IGetRecordFileByUniqueIdQuery,
            GetRecordFileByUniqueIdQuery(
                config=self.__config,
                get_connection=self.__get_connection,
                logger=logger
            )
        )

    async def unload(self) -> None:
        self.__dispatcher.delete_function(IGetRecordFileByUniqueIdQuery)
