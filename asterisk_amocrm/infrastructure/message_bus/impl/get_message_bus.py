from asyncio import AbstractEventLoop
from typing import Any
from typing import Mapping

from asterisk_amocrm.infrastructure import IGetCurrentAppVersionFunction
from asterisk_amocrm.infrastructure import ILogger
from asterisk_amocrm.infrastructure import ISelectableFactory
from asterisk_amocrm.infrastructure import ISelector
from asterisk_amocrm.infrastructure import SelectedComponentConfig
from asterisk_amocrm.infrastructure import SelectorImpl

from .instances import MemoryMessageBusFactory
from .instances import RabbitmqMessageBusFactory

from ..core import InitializableMessageBus

__all__ = [
    "get_message_bus",
]


def get_message_bus(
    settings: Mapping[str, Any],
    get_app_version_function: IGetCurrentAppVersionFunction,
    event_loop: AbstractEventLoop,
    logger: ILogger,
) -> InitializableMessageBus:

    selector: ISelector[ISelectableFactory[InitializableMessageBus]] = SelectorImpl()

    selector.add_item(
        MemoryMessageBusFactory(
            event_loop=event_loop,
            logger=logger,
        )
    )

    selector.add_item(
        RabbitmqMessageBusFactory(
            get_app_version_function=get_app_version_function,
            event_loop=event_loop,
            logger=logger,
        )
    )

    startup_config = SelectedComponentConfig(**settings)

    factory = selector.get_item(startup_config.type)
    instance = factory.get_instance(settings=startup_config.settings)

    return instance
