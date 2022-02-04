from asyncio import AbstractEventLoop
from typing import Any, Mapping
from asterisk_amocrm.infrastructure import (
    FactoryStoreImpl,
    IComponent,
    IDispatcher,
    IEventBus,
    IFactory,
    IFactoryStore,
    IKeyValueStorage,
    ILogger,
)

from .instances import Asterisk16ComponentFactory


__all__ = [
    "telephony_startup",
]


def telephony_startup(
    settings: Mapping[str, Any],
    dispatcher: IDispatcher,
    event_bus: IEventBus,
    storage: IKeyValueStorage,
    event_loop: AbstractEventLoop,
    logger: ILogger,
) -> IComponent:

    telephony_type = settings["type"]
    telephony_settings = settings["settings"]

    factory_store: IFactoryStore[IComponent] = FactoryStoreImpl()

    asterisk_16_factory: IFactory[IComponent] = Asterisk16ComponentFactory(
        dispatcher=dispatcher,
        storage=storage,
        event_bus=event_bus,
        event_loop=event_loop,
        logger=logger,
    )

    factory_store.register_factory(asterisk_16_factory)

    telephony_component = factory_store.get_instance(
        type=telephony_type,
        settings=telephony_settings,
    )

    return telephony_component
