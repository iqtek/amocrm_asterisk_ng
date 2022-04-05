from typing import Optional


__all__ = [
    "IKeyValueStorage",
]


class IKeyValueStorage:

    __slots__ = ()

    async def set_expire(self, key: str, expire: float) -> None:
        """
        Set an expiration time for the key.

        :param key: Key that will expire.
        :param expire: Will set after how many seconds the key will expire.
        :raises KeyError: If key is missing in the storage.
        :raises ConnectionError: if failure to connect to storage.
        """
        raise NotImplementedError()

    async def set(self, key: str, value: str, expire: Optional[float] = None) -> None:
        """
        Set value for key.

        :param key: The key by which the value will be available.
        :param value: Set value.
        :param expire: Will set after how many seconds the key will expire.
        :raises KeyError: If key has already in the storage.
        :raises ValueError: If Invalid value.
        :raises ConnectionError: if failure to connect to storage.
        """
        raise NotImplementedError()

    async def get(self, key: str) -> str:
        """
        Get the value by key.

        :param key: The key by which the value is contained.
        :raises KeyError: If key is missing in the storage.
        :raises ConnectionError: if failure to connect to storage.
        """
        raise NotImplementedError()

    async def update(self, key: str, value: str, expire: Optional[float] = None) -> None:
        """
        Update value for key.

        :param key: The key by which the value will be available.
        :param value: Set value.
        :param expire: Will set after how many seconds the key will expire.
        :raises KeyError: If key is missing in the storage.
        :raises ValueError: If Invalid value.
        :raises ConnectionError: if failure to connect to storage.
        """
        raise NotImplementedError()

    async def delete(self, key: str) -> None:
        """
        Delete key from storage.

        :raises KeyError: If key is missing in the storage.
        :raises ConnectionError: if failure to connect to storage.
        """
        raise NotImplementedError()
