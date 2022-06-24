from asyncio import AbstractEventLoop
from typing import Any
from typing import Mapping
from typing import Optional

from aiomysql import connect
from aiomysql.connection import Connection

from glassio.mixins import IFactory

from .MySqlConfigModel import MySqlConfig


__all__ = [
    "MySqlConnectionFactoryImpl",
]


class MySqlConnectionFactoryImpl(IFactory[Connection]):

    __slots__ = (
        "__event_loop",
    )

    def __init__(
        self,
        event_loop: AbstractEventLoop,
    ) -> None:
        self.__event_loop = event_loop

    async def get_instance(
        self,
        settings: Optional[Mapping[str, Any]] = None,
    ) -> Connection:

        settings = settings or {}

        config = MySqlConfig(**settings)

        connection = await connect(
            host=str(config.host),
            port=config.port,
            user=config.user,
            password=config.password,
            db=config.database,
            loop=self.__event_loop,
        )
        return connection
