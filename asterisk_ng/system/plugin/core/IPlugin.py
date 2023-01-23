from typing import Any
from typing import Generic
from typing import Mapping
from typing import TypeVar


__all__ = ["IPlugin"]


T = TypeVar('T')


class IPlugin(Generic[T]):

    __slots__ = ()

    @property
    def interface(self) -> T:
        raise NotImplementedError()

    async def upload(self, settings: Mapping[str, Any]) -> None:
        raise NotImplementedError()

    async def reload(self, settings: Mapping[str, Any]) -> None:
        raise NotImplementedError()

    async def unload(self) -> None:
        raise NotImplementedError()
