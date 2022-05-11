from ...ioc_container import ioc
from .get_dispatcher import get_dispatcher
from ..core import IDispatcher
from ...logger import ILogger

__all__ = [
    "dispatcher_startup",
]


def dispatcher_startup() -> None:
    logger = ioc.get_instance(ILogger)
    dispatcher = get_dispatcher(logger)

    ioc.set_instance(
        key=IDispatcher,
        instance=dispatcher,
    )
