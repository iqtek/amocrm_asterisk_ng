from typing import Mapping
from typing import Any

from asterisk_amocrm.infrastructure import ILogger
from asterisk_amocrm.infrastructure import ISelectable

from .RedisConnectionFactory import RedisConnectionFactoryImpl
from .RedisKeyValueStorage import RedisKeyValueStorage
from .RedisStorageConfigModel import RedisStorageConfigModel

from ....core import IKeyValueStorageFactory


__all__ = [
    "RedisKeyValueStorageFactory",
]


class RedisKeyValueStorageFactory(IKeyValueStorageFactory, ISelectable):

    __slots__ = (
        "__logger",
        "__connection",
        "__settings",
    )

    def __init__(
        self,
        settings: Mapping[str, Any],
        logger: ILogger,
    ) -> None:
        self.__settings = settings
        self.__logger = logger

        config = RedisStorageConfigModel()
        redis_conn_factory = RedisConnectionFactoryImpl(config)

        self.__connection = redis_conn_factory.get_instance()

    def unique_tag(self) -> str:
        return "redis"

    def get_instance(self, prefix: str = None) -> RedisKeyValueStorage:

        return RedisKeyValueStorage(
            connection=self.__connection,
            prefix=prefix,
            logger=self.__logger,
        )
