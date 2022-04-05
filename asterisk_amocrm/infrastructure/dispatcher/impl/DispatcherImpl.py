from typing import MutableMapping
from typing import Type
from typing import TypeVar
from ..core import IDispatcher
from ..core import IFunction


__all__ = [
    "DispatcherImpl"
]

F = TypeVar('F', bound=IFunction)


T = TypeVar('T')


class DispatcherImpl(IDispatcher):

    __slots__ = (
        "__functions",
    )

    def __init__(self) -> None:
        self.__functions: MutableMapping[Type[T], T] = {}

    def add_function(
        self,
        function_type: Type[F],
        function: F
    ) -> None:
        self.__functions[function_type] = function

    def delete_function(
        self,
        function_type: Type[F]
    ) -> None:
        try:
            self.__functions.pop(function_type)
        except KeyError:
            raise KeyError(
                "Unable to remove a non-existent function:"
                f" '{function_type}'."
            )

    def get_function(self, function_type: Type[F]) -> F:

        functions = self.__functions

        class FunctionProxy(function_type):

            async def __call__(self, *args, **kwargs):
                nonlocal functions
                try:
                    function = functions[function_type]
                except KeyError:
                    raise KeyError(
                        "Unable to get a non-existent function:"
                        f" '{function_type}'."
                    )
                return await function(*args, **kwargs)

        return FunctionProxy()
