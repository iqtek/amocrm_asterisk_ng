from .DispatcherImpl import DispatcherImpl
from ...logger import ILogger
from ..core import IDispatcher


__all__ = [
    "get_dispatcher",
]


def get_dispatcher(logger: ILogger) -> IDispatcher:
    return DispatcherImpl(logger=logger)
