from typing import Optional

from .IMakeContextSnapshotFunction import ContextSnapshot


__all__ = [
    "ISetContextVarsFunction",
]


class ISetContextVarsFunction:

    __slots__ = ()

    def __call__(self, snapshot: Optional[ContextSnapshot] = None) -> None:
        raise NotImplementedError()
