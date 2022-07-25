from glassio.dispatcher import IDispatcher
from glassio.event_bus import IEventBus
from glassio.logger import ILogger

from .get_scenario_factory import get_scenario_factory
from .get_scenario_settings import get_scenario_settings
from ..core import IScenario


__all__ = [
    "get_scenario",
]


def get_scenario(
    scenario_name: str,
    scenario_config_dir: str,
    event_bus: IEventBus,
    dispatcher: IDispatcher,
    logger: ILogger,
) -> IScenario:

    settings = get_scenario_settings(scenario_name, scenario_config_dir)

    scenario_factory_type = get_scenario_factory(scenario_name)

    factory = scenario_factory_type()
    factory.initialize(
        event_bus=event_bus,
        dispatcher=dispatcher,
        logger=logger,
    )

    scenario = factory.get_instance(settings=settings)
    return scenario
