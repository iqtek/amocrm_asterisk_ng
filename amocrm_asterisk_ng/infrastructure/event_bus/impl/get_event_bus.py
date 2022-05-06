from asyncio import AbstractEventLoop
from typing import Any
from typing import Mapping

from amocrm_asterisk_ng.infrastructure import ISelectableFactory
from amocrm_asterisk_ng.infrastructure import ISelector
from amocrm_asterisk_ng.infrastructure import SelectedComponentConfig
from amocrm_asterisk_ng.infrastructure import SelectorImpl
from amocrm_asterisk_ng.infrastructure import ILogger

from .instances import MemoryEventBusFactory

from ..core import InitializableEventBus


__all__ = [
    "get_event_bus",
]


def get_event_bus(
    settings: Mapping[str, Any],
    event_loop: AbstractEventLoop,
    logger: ILogger,
) -> InitializableEventBus:

    selector: ISelector[ISelectableFactory[InitializableEventBus]] = SelectorImpl()

    selector.add_item(
        MemoryEventBusFactory(
            event_loop=event_loop,
            logger=logger,
        )
    )

    startup_config = SelectedComponentConfig(**settings)

    factory = selector.get_item(startup_config.type)
    instance = factory.get_instance(settings=startup_config.settings)

    return instance
