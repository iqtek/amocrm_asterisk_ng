from typing import TypeVar
from typing import Generic


__all__ = [
    "IValueFactory",
]


T = TypeVar("T")


class IValueFactory(Generic[T]):

    __slots__ = ()

    def __call__(self) -> T:
        raise NotImplementedError()
