from typing import Any
from typing import Mapping

from fastapi import FastAPI

from amocrm_asterisk_ng.infrastructure import IDispatcher
from amocrm_asterisk_ng.infrastructure import ILogger
from amocrm_asterisk_ng.infrastructure import InitializableComponent
from amocrm_asterisk_ng.infrastructure import InitializableEventBus
from amocrm_asterisk_ng.infrastructure import ioc
from amocrm_asterisk_ng.infrastructure import ISelector
from amocrm_asterisk_ng.infrastructure import SelectedComponentConfig
from amocrm_asterisk_ng.infrastructure import SelectorImpl

from .amocrm import AmocrmComponentFactory


__all__ = [
    "crm_startup"
]


def crm_startup(
    settings: Mapping[str, Any],
) -> None:

    app = ioc.get_instance(FastAPI)
    event_bus = ioc.get_instance(InitializableEventBus)
    dispatcher = ioc.get_instance(IDispatcher)
    logger = ioc.get_instance(ILogger)

    startup_config = SelectedComponentConfig(**settings)

    selector: ISelector[InitializableComponent] = SelectorImpl()

    amocrm_factory = AmocrmComponentFactory(
        app=app,
        dispatcher=dispatcher,
        event_bus=event_bus,
        logger=logger,
    )

    selector.add_item(amocrm_factory)

    factory = selector.get_item(unique_tag=startup_config.type)
    crm_component = factory.get_instance(
        settings=startup_config.settings,
    )
    control_components = ioc.get("control_components")
    control_components.append(crm_component)
