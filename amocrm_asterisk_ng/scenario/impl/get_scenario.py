from typing import Mapping
from typing import Any

from glassio.dispatcher import IDispatcher
from glassio.event_bus import IEventBus
from glassio.logger import ILogger

from .get_scenario_factory import get_scenario_factory
from ..core import IScenario


__all__ = [
    "get_scenario",
]


def get_scenario(
    scenario_name: str,
    settings: Mapping[str, Any],
    event_bus: IEventBus,
    dispatcher: IDispatcher,
    logger: ILogger,
) -> IScenario:

    scenario_factory_type = get_scenario_factory(scenario_name)

    factory = scenario_factory_type()
    factory.initialize(
        event_bus=event_bus,
        dispatcher=dispatcher,
        logger=logger,
    )

    scenario = factory.get_instance(settings=settings)
    return scenario
