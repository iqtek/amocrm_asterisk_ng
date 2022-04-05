from typing import NewType


__all__ = [
    "IMakeContextSnapshotFunction",
    "ContextSnapshot",
]


class ContextSnapshot(dict):
    pass

# ContextSnapshot = NewType("ContextSnapshot", tp=dict)


class IMakeContextSnapshotFunction:

    def __call__(self) -> ContextSnapshot:
        raise NotImplementedError()
