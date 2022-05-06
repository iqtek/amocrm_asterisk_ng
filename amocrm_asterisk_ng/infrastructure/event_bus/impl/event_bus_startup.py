from asyncio import AbstractEventLoop
from typing import Any
from typing import Mapping

from amocrm_asterisk_ng.infrastructure import ioc
from amocrm_asterisk_ng.infrastructure.logger import ILogger


from .get_event_bus import get_event_bus
from ..core import InitializableEventBus


__all__ = [
    "event_bus_startup",
]


def event_bus_startup(
    settings: Mapping[str, Any],
) -> None:

    event_loop = ioc.get_instance(AbstractEventLoop)
    logger = ioc.get_instance(ILogger)

    instance = get_event_bus(
        settings=settings,
        event_loop=event_loop,
        logger=logger,
    )

    ioc.set_instance(
        key=InitializableEventBus,
        instance=instance,
    )
