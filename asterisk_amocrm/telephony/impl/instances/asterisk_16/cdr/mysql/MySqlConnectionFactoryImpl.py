from asyncio import AbstractEventLoop
from typing import Any, Mapping

import aiomysql
from aiomysql.connection import Connection

from .MySqlConfigModel import MySqlConfigModel


__all__ = [
    "MySqlConnectionFactoryImpl",
]


class MySqlConnectionFactoryImpl:

    def __init__(
        self,
        event_loop: AbstractEventLoop,
    ) -> None:
        self.__event_loop = event_loop

    async def get_instance(self, settings: Mapping[str, Any]) -> Connection:
        config = MySqlConfigModel(**settings)
        connection = await aiomysql.connect(
            host=str(config.host),
            port=config.port,
            user=config.user,
            password=config.password,
            db=config.database,
            loop=self.__event_loop,
        )
        return connection
