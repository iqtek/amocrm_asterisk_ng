from collections import defaultdict
from inspect import iscoroutinefunction

from typing import Any
from typing import Collection
from typing import Mapping
from typing import MutableMapping
from typing import MutableSequence
from typing import Optional
from typing import Sequence
from typing import Type
from typing import TypeVar

from asterisk_ng.system.logger import ILogger

from ..core import DispatcherException
from ..core import FunctionNotFoundException
from ..core import IDispatcher
from ..core import IFunction
from ..core import IFunctionDecorator


__all__ = [
    "LocalDispatcher"
]


F = TypeVar('F', bound=IFunction)


class LocalDispatcher(IDispatcher):

    __slots__ = (
        "__functions",
        "__function_decorators",
        "__logger",
    )

    def __init__(self, logger: ILogger) -> None:
        self.__functions: MutableMapping[Type[F], F] = {}
        self.__function_decorators: MutableMapping[Type[F], MutableSequence[IFunctionDecorator[F]]] = defaultdict(list)
        self.__logger = logger

    def add_function(
        self,
        function_type: Type[F],
        function: F,
        forced: bool = False,
    ) -> None:
        if function_type in self.__functions.keys() and not forced:
            raise DispatcherException(
                "The function has already been added."
            )

        if not isinstance(function, function_type):
            raise DispatcherException(
                "The function does not match the specified function_type."
            )

        if not issubclass(function_type, IFunction):
            raise DispatcherException(
                "The specified function_type is not an inheritor of IFunction."
            )

        if not iscoroutinefunction(function.__call__):
            raise DispatcherException(
                "The function must be asynchronous."
            )

        self.__functions[function_type] = function

    def delete_function(
        self,
        function_type: Type[F]
    ) -> None:
        try:
            self.__functions.pop(function_type)
        except KeyError:
            raise FunctionNotFoundException(
                f"Unable to delete a non-existent function: `{function_type}`."
            )

    def __get_function(self, function_type: Type[F]) -> F:
        try:
            return self.__functions[function_type]
        except KeyError:
            raise FunctionNotFoundException(
                f"Unable to get a non-existent function: `{function_type}`."
            )

    def get_function(self, function_type: Type[F]) -> F:
        logger = self.__logger
        function_decorators = self.__function_decorators
        get_function = self.__get_function

        class FunctionProxy(function_type):

            __slots__ = ()

            async def __call__(self, *args, **kwargs):
                nonlocal function_type, logger, function_decorators, get_function

                function = get_function(function_type)
                for decorator in function_decorators[function_type]:
                    function = decorator(function)

                try:
                    result = await function(*args, **kwargs)
                except Exception as exc:
                    await logger.debug(
                        f"Call function: `{type(function)}`, args: {args}, kwargs: {kwargs}, "
                        f"exception: `{exc!r}`."
                    )
                    raise exc
                else:
                    await logger.debug(
                        f"Call function: `{type(function)}`, args: {args}, kwargs: {kwargs}, "
                        f"result: `{result!r}`."
                    )
                    return result

        return FunctionProxy()

    def get_function_types(self) -> Collection[Type[IFunction]]:
        return self.__functions.keys()

    async def call_function(
        self,
        function_type: Type[F],
        args: Optional[Sequence[Any]] = None,
        kwargs: Optional[Mapping[str, Any]] = None
    ) -> Any:
        args = args or ()
        kwargs = kwargs or {}
        function = self.get_function(function_type)
        return await function(*args, **kwargs)

    def add_function_decorator(
        self,
        function: Type[IFunction],
        decorator: IFunctionDecorator,
    ) -> None:
        self.__function_decorators[function].insert(0, decorator)

    def delete_function_decorator(
        self,
        function: Type[IFunction],
        decorator: IFunctionDecorator,
    ) -> None:
        try:
            self.__function_decorators[function].remove(decorator)
        except ValueError:
            raise DispatcherException(
                f"There is no decorator: `{decorator}` for the function: `{function}`."
            )
