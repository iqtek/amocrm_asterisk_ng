import yaml

from amocrm_asterisk_ng.infrastructure import IDispatcher
from amocrm_asterisk_ng.infrastructure import IEventBus
from amocrm_asterisk_ng.infrastructure import ILogger

from .classic import ClassicScenarioFactory
from ..core import IScenario


__all__ = [
    "get_scenario",
]


def get_scenario(
    scenario_name: str,
    scenario_configs_dir: str,
    event_bus: IEventBus,
    dispatcher: IDispatcher,
    logger: ILogger,
) -> IScenario:

    scenario_configs_dir = scenario_configs_dir.rstrip('/')

    if scenario_name != "classic":
        raise Exception("Integration does not support scenario switching yet.")

    with open(f"{scenario_configs_dir}/{scenario_name}_scenario.yml") as scenario_config_file:
        settings = yaml.safe_load(scenario_config_file)

    factory = ClassicScenarioFactory(
        event_bus=event_bus,
        dispatcher=dispatcher,
        logger=logger,
    )

    scenario = factory.get_instance(settings=settings)

    return scenario
