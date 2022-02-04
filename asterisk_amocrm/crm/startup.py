from typing import (
    Mapping,
    Any,
)
from fastapi import FastAPI
from asterisk_amocrm.infrastructure import (
    IComponent,
    IDispatcher,
    IEventBus,
    ILogger,
    IFactory,
    IFactoryStore,
    FactoryStoreImpl,
    IKeyValueStorage,
)
from .amocrm import AmocrmComponentFactory


__all__ = [
    "crm_startup"
]


def crm_startup(
    settings: Mapping[str, Any],
    app: FastAPI,
    event_bus: IEventBus,
    dispatcher: IDispatcher,
    storage: IKeyValueStorage,
    logger: ILogger,
) -> IComponent:
    crm_type = settings["type"]
    crm_settings = settings["settings"]

    factory_store: IFactoryStore[IComponent] = FactoryStoreImpl()

    amocrm_factory: IFactory[IComponent] = AmocrmComponentFactory(
        app=app,
        dispatcher=dispatcher,
        event_bus=event_bus,
        storage=storage,
        logger=logger,
    )
    factory_store.register_factory(amocrm_factory)

    crm_component = factory_store.get_instance(
        type=crm_type,
        settings=crm_settings,
    )

    return crm_component
