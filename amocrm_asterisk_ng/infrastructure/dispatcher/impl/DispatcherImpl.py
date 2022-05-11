from typing import MutableMapping
from typing import Type
from inspect import iscoroutinefunction
from typing import TypeVar
from ..core import IDispatcher
from ..core import IFunction

from ...logger import ILogger


__all__ = [
    "DispatcherImpl"
]

F = TypeVar('F', bound=IFunction)


T = TypeVar('T')


class DispatcherImpl(IDispatcher):

    __slots__ = (
        "__functions",
        "__logger",
    )

    def __init__(self, logger: ILogger) -> None:
        self.__functions: MutableMapping[Type[T], T] = {}
        self.__logger = logger

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

        logger = self.__logger

        functions = self.__functions

        if iscoroutinefunction(function_type.__call__):
            class AsynchronousFunctionProxy(function_type):

                async def __call__(self, *args, **kwargs):
                    nonlocal functions
                    try:
                        function = functions[function_type]
                    except KeyError:
                        raise KeyError(
                            "Unable to get a non-existent function:"
                            f" '{function_type}'."
                        )
                    try:
                        result = await function(*args, **kwargs)
                    except Exception as exc:
                        logger.debug(
                            f"Dispatcher: call function: `{type(function)}`; args: `{args}`; kwargs: `{kwargs}`; "
                            f"exc: `{exc!r}`."
                        )
                    else:
                        logger.debug(
                            f"Dispatcher: call function: `{type(function)}`; args: {args}; kwargs: {kwargs}; "
                            f"result: `{result}`."
                        )
                        return result
            return AsynchronousFunctionProxy()

        class SynchronousFunctionProxy(function_type):

            def __call__(self, *args, **kwargs):
                nonlocal functions
                try:
                    function = functions[function_type]
                except KeyError:
                    raise KeyError(
                        "Unable to get a non-existent function:"
                        f" '{function_type}'."
                    )
                try:
                    result = function(*args, **kwargs)
                except Exception as exc:
                    logger.debug(
                        f"Dispatcher: call function: `{type(function)}`; args: {args}; kwargs: {kwargs}; "
                        f"exc: `{exc!r}`."
                    )
                else:
                    logger.debug(
                        f"Dispatcher: call function: `{type(function)}`; args: {args}; kwargs: {kwargs}; "
                        f"result: `{result}`."
                    )
                    return result

        return SynchronousFunctionProxy()
