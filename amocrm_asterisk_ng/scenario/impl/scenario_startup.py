from typing import Mapping
from typing import Any


from glassio.dispatcher import IDispatcher
from glassio.event_bus import InitializableEventBus
from glassio.logger import ILogger

from amocrm_asterisk_ng.infrastructure import ioc

from .get_scenario import get_scenario
from ..core import IScenario


__all__ = [
    "scenario_startup",
]


def scenario_startup(scenario_name: str, settings: Mapping[str, Any]) -> None:

    event_bus = ioc.get_instance(InitializableEventBus)
    dispatcher = ioc.get_instance(IDispatcher)
    logger = ioc.get_instance(ILogger)

    scenario = get_scenario(
        scenario_name=scenario_name,
        settings=settings,
        event_bus=event_bus,
        dispatcher=dispatcher,
        logger=logger,
    )

    ioc.set_instance(IScenario, scenario)
