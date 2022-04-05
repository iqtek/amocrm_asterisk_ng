from typing import Generic
from typing import TypeVar


__all__ = [
    "IFunction",
]


T = TypeVar('T')


class IFunction(Generic[T]):

    __slots__ = ()

    async def __call__(self, *args, **kwargs) -> T:
        raise NotImplementedError()
