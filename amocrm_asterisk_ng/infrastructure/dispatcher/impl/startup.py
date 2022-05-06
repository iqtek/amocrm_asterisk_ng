from ...ioc_container import ioc
from .get_dispatcher import get_dispatcher
from ..core import IDispatcher


__all__ = [
    "dispatcher_startup",
]


def dispatcher_startup() -> None:

    dispatcher = get_dispatcher()

    ioc.set_instance(
        key=IDispatcher,
        instance=dispatcher,
    )
