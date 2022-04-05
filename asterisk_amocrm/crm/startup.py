from typing import Any
from typing import Mapping

from fastapi import FastAPI

from asterisk_amocrm.infrastructure import IDispatcher
from asterisk_amocrm.infrastructure import IKeyValueStorageFactory
from asterisk_amocrm.infrastructure import ILogger
from asterisk_amocrm.infrastructure import InitializableComponent
from asterisk_amocrm.infrastructure import InitializableEventBus
from asterisk_amocrm.infrastructure import ISetContextVarsFunction
from asterisk_amocrm.infrastructure import ioc
from asterisk_amocrm.infrastructure import ISelector
from asterisk_amocrm.infrastructure import SelectedComponentConfig
from asterisk_amocrm.infrastructure import SelectorImpl
from .amocrm import AmocrmComponentFactory


__all__ = [
    "crm_startup"
]


def crm_startup(
    settings: Mapping[str, Any],
) -> InitializableComponent:

    app = ioc.get_instance(FastAPI)
    event_bus = ioc.get_instance(InitializableEventBus)
    dispatcher = ioc.get_instance(IDispatcher)
    storage_factory = ioc.get_instance(IKeyValueStorageFactory)
    logger = ioc.get_instance(ILogger)
    set_context_vars_function = ioc.get_instance(ISetContextVarsFunction)

    startup_config = SelectedComponentConfig(**settings)

    selector: ISelector[InitializableComponent] = SelectorImpl()

    amocrm_factory = AmocrmComponentFactory(
        app=app,
        dispatcher=dispatcher,
        event_bus=event_bus,
        storage_factory=storage_factory,
        set_context_vars_function=set_context_vars_function,
        logger=logger,
    )

    selector.add_item(amocrm_factory)

    factory = selector.get_item(unique_tag=startup_config.type)
    crm_component = factory.get_instance(
        settings=startup_config.settings,
    )
    return crm_component
