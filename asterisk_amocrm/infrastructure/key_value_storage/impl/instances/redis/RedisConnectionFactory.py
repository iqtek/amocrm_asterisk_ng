import aioredis
from aioredis import (
    Redis,
)
from .RedisStorageConfigModel import (
    RedisStorageConfigModel,
)


__all__ = [
    "RedisConnectionFactoryImpl",
]


class RedisConnectionFactoryImpl:

    def __init__(self, config: RedisStorageConfigModel) -> None:
        self.__config = config

    def get_instance(self) -> Redis:
        try:
            redis = aioredis.from_url(
                f"redis://{self.__config.host}",
                port=self.__config.port,
                db=self.__config.database
            )
        except Exception as e:
            raise ConnectionError(
                "Error creating connection to Redis."
            ) from e
        return redis
