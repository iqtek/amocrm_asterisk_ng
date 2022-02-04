from typing import (
    Optional,
    Mapping,
    Any,
)
from asterisk_amocrm.infrastructure.logger import (
    ILogger,
)
from ....core import (
    IKeyValueStorageFactory,
    IKeyValueStorage,
)
from .RedisConnectionFactory import RedisConnectionFactoryImpl
from .RedisStorageConfigModel import RedisStorageConfigModel
from .RedisKeyValueStorage import RedisKeyValueStorage


__all__ = [
    "RedisKeyValueStorageFactory",
]


class RedisKeyValueStorageFactory(IKeyValueStorageFactory):

    __slots__ = (
        "__logger",
        "__settings",
        "__config",
    )

    def __init__(
        self,
        logger: ILogger,
        settings: Optional[Mapping[str, Any]] = None,
        config: Optional[RedisStorageConfigModel] = None,
    ) -> None:
        self.__logger = logger
        self.__config = config
        self.__settings = settings or {}

    @classmethod
    def type(cls) -> str:
        return "redis"

    def get_instance(self, prefix: str = None) -> RedisKeyValueStorage:

        if not self.__config or not isinstance(self.__config, RedisStorageConfigModel):
            self.__config = RedisStorageConfigModel(**self.__settings)

        redis_conn_factory = RedisConnectionFactoryImpl(self.__config)
        connection = redis_conn_factory.get_instance()

        return RedisKeyValueStorage(
            connection=connection,
            prefix=prefix,
            logger=self.__logger,
        )
