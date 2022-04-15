from contextvars import ContextVar
from typing import Collection

from ..core import ContextSnapshot
from ..core import IMakeContextSnapshotFunction


__all__ = [
    "MakeContextSnapshotFunction",
]


class MakeContextSnapshotFunction(IMakeContextSnapshotFunction):

    __slots__ = (
        "__variables",
    )

    def __init__(self, variables: Collection[ContextVar]) -> None:
        self.__variables = variables

    def __call__(self) -> ContextSnapshot:

        snapshot = ContextSnapshot()

        for variable in self.__variables:
            key = variable.name
            value = variable.get(None)
            snapshot[key] = value

        return snapshot
