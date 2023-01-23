from typing import ClassVar
from typing import Optional

from aioredis import Redis
from asterisk_ng.system.logger import ILogger

from ...core import IKeyValueStorage


__all__ = ["RedisKeyValueStorage"]


class RedisKeyValueStorage(IKeyValueStorage):

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
        super().__init__()
        self.__connection = connection
        self.__logger = logger
        self.__prefix = f"{prefix or ''}{self.__DELIMITER}"

    def __get_full_key(self, key: str) -> str:
        return self.__prefix + key

    async def set_expire(self, key: str, expire: float) -> None:
        full_key = self.__get_full_key(key)
        keys = await self.__connection.keys(full_key)
        if full_key.encode('utf-8') not in keys:
            raise KeyError(f"The key: `{key}` missing.")
        await self.__connection.expire(full_key, round(expire))
        await self.__logger.debug(f"Set expiration key: `{key}` expire: `{expire}`.")

    async def set(self, key: str, value: str, expire: Optional[float] = None) -> None:
        full_key = self.__get_full_key(key)

        result = await self.__connection.set(full_key, value)
        if not result:
            raise KeyError(f"The key: `{key}` missing.")

        await self.__logger.debug(f"Set value: `{value}` by key: `{key}`.")
        if expire is not None:
            await self.set_expire(key, expire)

    async def get(self, key: str) -> str:
        full_key = self.__get_full_key(key)
        result = await self.__connection.get(full_key)
        if result is None:
            raise KeyError(f"The key: `{key}` is missing.")
        str_result = result.decode("utf-8")
        return str_result

    async def delete(self, key: str) -> None:
        full_key = self.__get_full_key(key)
        result = await self.__connection.delete(full_key)
        if not result:
            raise KeyError(f"The key: `{key}` is missing.")
        await self.__logger.debug(f"Delete key: `{full_key}`.")
