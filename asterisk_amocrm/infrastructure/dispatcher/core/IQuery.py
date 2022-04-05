from typing import TypeVar

from .IFunction import IFunction


__all__ = [
    "IQuery",
]


T = TypeVar('T')


class IQuery(IFunction[T]):

    __slots__ = ()

    async def __call__(self, *args, **kwargs) -> T:
        raise NotImplementedError()
