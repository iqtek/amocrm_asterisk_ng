from typing import Optional


__all__ = ["IKeyValueStorage"]


class IKeyValueStorage:

    __slots__ = ()

    async def set_expire(self, key: str, expire: float) -> None:
        raise NotImplementedError()

    async def set(self, key: str, value: str, expire: Optional[float] = None) -> None:
        raise NotImplementedError()

    async def get(self, key: str) -> str:
        raise NotImplementedError()

    async def delete(self, key: str) -> None:
        raise NotImplementedError()
