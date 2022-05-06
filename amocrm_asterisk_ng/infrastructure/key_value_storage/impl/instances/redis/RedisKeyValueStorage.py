from typing import Optional
from typing import ClassVar

from aioredis import Redis

from amocrm_asterisk_ng.infrastructure import ILogger
from ....core import InitializableKeyValueStorage


__all__ = [
    "RedisKeyValueStorage",
]


class RedisKeyValueStorage(InitializableKeyValueStorage):

    __slots__ = (
        "__connection",
        "__prefix",
        "__logger",
    )

    __DELIMITER: ClassVar[str] = '-'

    def __init__(
        self,
        connection: Redis,
        logger: ILogger,
        prefix: Optional[str] = None,
    ) -> None:
        self.__connection = connection
        self.__logger = logger
        if not prefix:
            prefix = ""
        self.__prefix = prefix + self.__DELIMITER

    def __get_full_key(self, key: str) -> str:
        return self.__prefix + key

    async def initialize(self) -> None:
        await self.__connection.initialize()

    async def deinitialize(self) -> None:
        await self.__connection.close()

    async def set_expire(self, key: str, expire: float) -> None:
        full_key = self.__get_full_key(key)
        keys = await self.__connection.keys(full_key)
        if full_key.encode('utf-8') not in keys:
            raise KeyError(
                "RedisKeyValueStorage: "
                "Could not update expiration for key. "
                f"The key={key} missing."
            )

        await self.__connection.expire(full_key, round(expire))
        self.__logger.debug(
            "RedisKeyValueStorage: "
            "Key expiration updated. "
            f"The key={key} expire={expire}."
        )

    async def set(self, key: str, value: str, expire: Optional[float] = None) -> None:
        full_key = self.__get_full_key(key)
        keys = await self.__connection.keys(full_key)
        if full_key.encode('utf-8') in keys:
            raise LookupError(
                "RedisKeyValueStorage: "
                "Could not set value for key. "
                f"The key={key} is already exists."
            )
        result = await self.__connection.set(full_key, value)
        if not result:
            raise ValueError(
                "RedisKeyValueStorage: "
                f"Could not set value={value} by key={key}."
            )
        self.__logger.debug(
            "RedisKeyValueStorage: "
            f"Set value={value} by key={key}."
        )
        if expire is not None:
            await self.set_expire(key, expire)

    async def get(self, key: str) -> str:
        full_key = self.__get_full_key(key)
        result = await self.__connection.get(full_key)
        if result is None:
            raise KeyError(
                "RedisKeyValueStorage: "
                "Failed to get value by key. "
                f"The key={key} is missing."
            )
        str_result = result.decode("utf-8")
        return str_result

    async def update(self, key: str, value: str, expire: Optional[float] = None) -> None:
        full_key = self.__get_full_key(key)
        keys = await self.__connection.keys(full_key)
        if full_key.encode('utf-8') not in keys:
            raise KeyError(
                "RedisKeyValueStorage: "
                "Could not update value for key. "
                f"The key={full_key} is missing."
            )

        result = await self.__connection.set(full_key, value)
        if not result:
            raise ValueError(
                "RedisKeyValueStorage: "
                f"Could not update value={value} by key={key}."
            )
        self.__logger.debug(
            "RedisKeyValueStorage: "
            f"Update value={value} by key={key}."
        )
        if expire is not None:
            await self.set_expire(key, expire)

    async def delete(self, key: str) -> None:
        full_key = self.__get_full_key(key)
        result = await self.__connection.delete(full_key)
        if not result:
            raise KeyError(
                "RedisKeyValueStorage: "
                f"Cannot delete value by full_key={full_key} ."
            )
        self.__logger.debug(f"RedisKeyValueStorage: Delete key={key} .")
