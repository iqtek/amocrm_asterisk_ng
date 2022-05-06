from typing import Type
from typing import TypeVar

from .ICommand import ICommand
from .IFunction import IFunction
from .IQuery import IQuery


__all__ = [
    "IDispatcher",
]


F = TypeVar('F', bound=IFunction)


class IDispatcher:

    __slots__ = ()

    def add_function(
        self,
        function_type: Type[F],
        function: F,
    ) -> None:
        raise NotImplementedError()

    def delete_function(self, function_type: Type[F]) -> None:
        raise NotImplementedError()

    def get_function(self, function_type: Type[F]) -> F:
        raise NotImplementedError()
