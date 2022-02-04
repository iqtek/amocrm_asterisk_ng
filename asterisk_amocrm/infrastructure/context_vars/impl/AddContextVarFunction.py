from typing import TypeVar
from contextvars import ContextVar
from ..core import (
    IValueFactory,
    IAddContextVarFunction,
)

__all__ = [
    "AddContextVarFunction",
]


T = TypeVar("T")


class AddContextVarFunction(IAddContextVarFunction):

    def __init__(
        self,
        context_var: ContextVar[T],
        value_factory: IValueFactory[T],
    ) -> None:
        self.__context_var = context_var
        self.__value_factory = value_factory

    def __call__(self, *args, **kwargs):
        new_value = self.__value_factory()
        self.__context_var.set(new_value)
