from importlib.util import find_spec
from importlib.util import module_from_spec
import os

from glassio.dispatcher import IDispatcher
from glassio.event_bus import IEventBus
from glassio.logger import ILogger
import yaml

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
    scenario_configs_file_path = f"{scenario_configs_dir}/{scenario_name}_scenario.yml"
    if not os.path.isfile(scenario_configs_file_path):
        raise Exception(
            f"There is no scenario: `{scenario_name}` configuration. "
            f"By path: `{scenario_configs_file_path}`."
        )

    with open(f"{scenario_configs_dir}/{scenario_name}_scenario.yml") as scenario_config_file:
        settings = yaml.safe_load(scenario_config_file)

    module_spec = find_spec(f".{scenario_name}", package=__name__[0:-13])
    if module_spec is None:
        raise Exception(
            f"The scenario module: `{scenario_name}` is missing."
        )
    scenario_module = module_from_spec(module_spec)
    module_spec.loader.exec_module(scenario_module)

    try:
        scenario_factory = scenario_module.SCENARIO_FACTORY
    except AttributeError:
        raise Exception(
            f"There is no variable SCENARIO_FACTORY in the scenario module."
        )

    factory = scenario_factory(
        event_bus=event_bus,
        dispatcher=dispatcher,
        logger=logger,
    )

    scenario = factory.get_instance(settings=settings)

    return scenario
