from contextvars import ContextVar
from logging import Filter
from typing import Collection


__all__ = [
    "TraceFilter",
]


class TraceFilter(Filter):

    def __init__(self, variables: Collection[ContextVar]) -> None:
        self.__variables = variables
        super().__init__()

    def filter(self, record):
        for variable in self.__variables:
            value = variable.get("")
            record.__setattr__(
                variable.name,
                value,
            )
        return True
