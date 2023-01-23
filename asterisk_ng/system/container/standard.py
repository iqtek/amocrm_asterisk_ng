from typing import Any
from typing import Optional
from typing import TypeVar

from .core import IResolver


__all__ = ["SingletonResolver"]


T = TypeVar('T')


class SingletonResolver(IResolver[T]):

    __slots__ = (
        "__instance",
    )

    def __init__(self, instance: T) -> None:
        self.__instance = instance

    def __call__(self, needy: Optional[Any] = None) -> T:
        return self.__instance
