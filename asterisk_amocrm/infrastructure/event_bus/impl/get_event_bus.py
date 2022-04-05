from asyncio import AbstractEventLoop
from typing import Any
from typing import Mapping

from asterisk_amocrm.infrastructure import InitializableMessageBus
from asterisk_amocrm.infrastructure import ISelectableFactory
from asterisk_amocrm.infrastructure import ISelector
from asterisk_amocrm.infrastructure import SelectedComponentConfig
from asterisk_amocrm.infrastructure import ISetContextVarsFunction
from asterisk_amocrm.infrastructure import IMakeContextSnapshotFunction
from asterisk_amocrm.infrastructure import SelectorImpl
from asterisk_amocrm.infrastructure import ILogger

from .instances import (
    ExtendedEventBusFactory,
    MemoryEventBusFactory,
)

from ..core import InitializableEventBus


__all__ = [
    "get_event_bus",
]


def get_event_bus(
    settings: Mapping[str, Any],
    message_bus: InitializableMessageBus,
    event_loop: AbstractEventLoop,
    logger: ILogger,
    set_context_vars_function: ISetContextVarsFunction,
    make_context_vars_snapshot: IMakeContextSnapshotFunction,
) -> InitializableEventBus:

    selector: ISelector[ISelectableFactory[InitializableEventBus]] = SelectorImpl()

    selector.add_item(
        MemoryEventBusFactory(
            event_loop=event_loop,
            logger=logger,
        )
    )

    selector.add_item(
        ExtendedEventBusFactory(
            message_bus=message_bus,
            event_loop=event_loop,
            logger=logger,
            set_context_vars_function=set_context_vars_function,
            make_context_vars_snapshot=make_context_vars_snapshot,
        )
    )

    startup_config = SelectedComponentConfig(**settings)

    factory = selector.get_item(startup_config.type)
    instance = factory.get_instance(settings=startup_config.settings)

    return instance
