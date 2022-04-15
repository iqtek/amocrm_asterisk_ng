from .DispatcherImpl import DispatcherImpl
from ..core import IDispatcher


__all__ = [
    "get_dispatcher",
]


def get_dispatcher() -> IDispatcher:
    return DispatcherImpl()
