from asyncio import AbstractEventLoop
from typing import Any
from typing import Mapping

from amocrm_asterisk_ng.infrastructure import ioc
from amocrm_asterisk_ng.infrastructure import ISelector
from amocrm_asterisk_ng.infrastructure import ISelectableFactory
from amocrm_asterisk_ng.infrastructure import SelectorImpl
from amocrm_asterisk_ng.infrastructure import InitializableComponent
from amocrm_asterisk_ng.infrastructure import IDispatcher
from amocrm_asterisk_ng.infrastructure import InitializableEventBus
from amocrm_asterisk_ng.infrastructure import IKeyValueStorageFactory
from amocrm_asterisk_ng.infrastructure import ILogger
from amocrm_asterisk_ng.infrastructure import SelectedComponentConfig
from amocrm_asterisk_ng.infrastructure import ISetContextVarsFunction

from .instances import Asterisk16ComponentFactory


__all__ = [
    "telephony_startup",
]


def telephony_startup(
    settings: Mapping[str, Any],
) -> InitializableComponent:

    startup_config = SelectedComponentConfig(**settings)

    dispatcher = ioc.get_instance(IDispatcher)
    event_bus = ioc.get_instance(InitializableEventBus)
    storage_factory = ioc.get_instance(IKeyValueStorageFactory)
    event_loop = ioc.get_instance(AbstractEventLoop)
    set_context_vars_function = ioc.get_instance(ISetContextVarsFunction)
    logger = ioc.get_instance(ILogger)

    selector: ISelector[ISelectableFactory[InitializableComponent]] = SelectorImpl()

    asterisk_16_factory = Asterisk16ComponentFactory(
        dispatcher=dispatcher,
        event_bus=event_bus,
        storage_factory=storage_factory,
        event_loop=event_loop,
        set_context_vars_function=set_context_vars_function,
        logger=logger,
    )

    selector.add_item(asterisk_16_factory)

    factory = selector.get_item(unique_tag=startup_config.type)
    telephony_component = factory.get_instance(
        settings=startup_config.settings,
    )

    return telephony_component
