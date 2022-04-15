from contextvars import ContextVar
from typing import MutableMapping
from typing import TypeVar
from typing import Optional

from ..core import ContextSnapshot
from ..core import ISetContextVarsFunction
from ..core import IValueFactory


__all__ = [
    "SetContextVarsFunction",
]


T = TypeVar("T")


class SetContextVarsFunction(ISetContextVarsFunction):

    __slots__ = (
        "__variable_names",
        "__variables",
    )

    def __init__(self) -> None:
        self.__variable_names: MutableMapping[str, ContextVar] = {}
        self.__variables: MutableMapping[ContextVar[T], IValueFactory[T]] = {}

    def add_context_var(
        self,
        context_var: ContextVar[T],
        value_factory: IValueFactory[T],
    ) -> None:
        self.__variable_names[context_var.name] = context_var
        self.__variables[context_var] = value_factory

    def __call__(self, snapshot: Optional[ContextSnapshot] = None) -> None:

        if snapshot is not None:
            for variable_name, value in snapshot.items():
                variable = self.__variable_names[variable_name]
                variable.set(value)
            return

        for variable, factory in self.__variables.items():
            variable.set(factory())
