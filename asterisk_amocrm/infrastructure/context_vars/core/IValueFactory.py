from typing import (
    TypeVar,
    Generic,
)

__all__ = [
    "IValueFactory",
]


T = TypeVar("T")


class IValueFactory(Generic[T]):

    def __call__(self) -> T:
        raise NotImplementedError()
