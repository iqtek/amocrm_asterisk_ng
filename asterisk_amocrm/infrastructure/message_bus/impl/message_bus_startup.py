from asyncio import AbstractEventLoop
from typing import Any
from typing import Mapping

from asterisk_amocrm.infrastructure import IGetCurrentAppVersionFunction
from asterisk_amocrm.infrastructure import ILogger
from asterisk_amocrm.infrastructure import ioc

from .get_message_bus import get_message_bus
from ..core import InitializableMessageBus


__all__ = [
    "message_bus_startup",
]


def message_bus_startup(
    settings: Mapping[str, Any],
) -> None:

    get_app_version_function = ioc.get_instance(IGetCurrentAppVersionFunction)
    event_loop = ioc.get_instance(AbstractEventLoop)
    logger = ioc.get_instance(ILogger)

    instance = get_message_bus(
        settings=settings,
        get_app_version_function=get_app_version_function,
        event_loop=event_loop,
        logger=logger,
    )

    ioc.set_instance(
        key=InitializableMessageBus,
        instance=instance,
    )
