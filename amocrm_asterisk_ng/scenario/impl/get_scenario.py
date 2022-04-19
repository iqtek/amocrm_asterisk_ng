import yaml

from amocrm_asterisk_ng.infrastructure import IDispatcher
from amocrm_asterisk_ng.infrastructure import IEventBus

from .classic import ClassicScenarioFactory
from ..core import IScenario


__all__ = [
    "get_scenario",
]


def get_scenario(
    scenario_name: str,
    event_bus: IEventBus,
    dispatcher: IDispatcher,
) -> IScenario:

    with open(f"configs/{scenario_name}_scenario.yml") as scenario_config_file:
        settings = yaml.safe_load(scenario_config_file)

    factory = ClassicScenarioFactory(
        event_bus=event_bus,
        dispatcher=dispatcher,
    )

    scenario = factory.get_instance(settings=settings)

    return scenario
