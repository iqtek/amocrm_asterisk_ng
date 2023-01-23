from typing import Any
from typing import Mapping
from typing import Optional

from asterisk_ng.system.components import AbstractInitializableComponent
from asterisk_ng.system.logger import ILogger

from .RedisKeyValueStorage import RedisKeyValueStorage
from .RedisStorageConfigModel import RedisStorageConfigModel
from .redis_connection_factory import redis_connection_factory

from ...core import IKeyValueStorage
from ...core import IKeyValueStorageFactory


__all__ = ["RedisKeyValueStorageFactory"]


class RedisKeyValueStorageFactory(IKeyValueStorageFactory, AbstractInitializableComponent):

    __slots__ = (
        "__logger",
        "__connection",
    )

    def __init__(
        self,
        settings: Mapping[str, Any],
        logger: ILogger,
    ) -> None:
        super().__init__(name="RedisKeyValueStorageFactory")
        self.__logger = logger
        self.__connection = redis_connection_factory(RedisStorageConfigModel(**settings))

    async def _initialize(self) -> None:
        await self.__connection.initialize()

    def __call__(self, prefix: str = None) -> IKeyValueStorage:
        return RedisKeyValueStorage(
            connection=self.__connection,
            prefix=prefix,
            logger=self.__logger,
        )

    async def _deinitialize(self, exception: Optional[Exception] = None) -> None:
        await self.__connection.close()
