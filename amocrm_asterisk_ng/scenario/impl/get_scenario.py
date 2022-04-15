from typing import Any
from typing import Mapping

from ..core import IScenario


__all__ = [
    "get_scenario",
]


def get_scenario(scenario_name: str, settings: Mapping[str, Any]) -> IScenario:
