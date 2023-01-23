from typing import Generic
from typing import TypeVar

from .functions import IFunction


__all__ = [
    "IFunctionDecorator",
]


F = TypeVar("F", bound=IFunction)


class IFunctionDecorator(Generic[F]):

    __slots__ = ()

    def __call__(self, function: F) -> IFunction:
        raise NotImplementedError()
