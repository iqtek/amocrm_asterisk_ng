from asyncio import AbstractEventLoop
from typing import Any
from typing import Mapping

from asterisk_amocrm.infrastructure import InitializableMessageBus
from asterisk_amocrm.infrastructure import ioc
from asterisk_amocrm.infrastructure.logger import ILogger
from asterisk_amocrm.infrastructure import ISetContextVarsFunction
from asterisk_amocrm.infrastructure import IMakeContextSnapshotFunction

from .get_event_bus import get_event_bus
from ..core import InitializableEventBus


__all__ = [
    "event_bus_startup",
]


def event_bus_startup(
    settings: Mapping[str, Any],
) -> None:

    message_bus = ioc.get_instance(InitializableMessageBus)
    event_loop = ioc.get_instance(AbstractEventLoop)
    logger = ioc.get_instance(ILogger)

    set_context_vars_function = ioc.get_instance(ISetContextVarsFunction)
    make_context_vars_snapshot = ioc.get_instance(IMakeContextSnapshotFunction)

    instance = get_event_bus(
        settings=settings,
        message_bus=message_bus,
        event_loop=event_loop,
        logger=logger,
        set_context_vars_function=set_context_vars_function,
        make_context_vars_snapshot=make_context_vars_snapshot,
    )

    ioc.set_instance(
        key=InitializableEventBus,
        instance=instance,
    )
