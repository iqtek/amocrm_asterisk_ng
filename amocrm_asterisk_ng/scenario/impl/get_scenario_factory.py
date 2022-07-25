from importlib.util import find_spec
from importlib.util import module_from_spec
from typing import Type

from ..core import IScenarioFactory


__all__ = [
    "get_scenario_factory",
]


def get_scenario_factory(
    scenario_name: str,
) -> Type[IScenarioFactory]:

    package_name = __name__.rstrip(".get_scenario_factory")
    module_spec = find_spec(f".scenarios.{scenario_name}", package=package_name)
    if module_spec is None:
        raise Exception(
            f"The scenario module: `{scenario_name}` is missing."
        )

    scenario_module = module_from_spec(module_spec)
    module_spec.loader.exec_module(scenario_module)

    try:
        return scenario_module.SCENARIO_FACTORY
    except AttributeError:
        raise Exception(
            f"There is no variable `SCENARIO_FACTORY` in the scenario module."
        )
