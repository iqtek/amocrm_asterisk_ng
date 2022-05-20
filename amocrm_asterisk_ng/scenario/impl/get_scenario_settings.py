import os
from typing import Any
from typing import Mapping

import yaml


__all__ = [
    "get_scenario_settings",
]


def get_scenario_settings(
    scenario_name: str,
    scenario_config_dir: str
) -> Mapping[str, Any]:
    scenario_configs_dir = scenario_config_dir.rstrip('/')
    scenario_configs_file_path = f"{scenario_configs_dir}/{scenario_name}_scenario.yml"
    if not os.path.isfile(scenario_configs_file_path):
        raise Exception(
            f"There is no scenario: `{scenario_name}` configuration "
            f"by path: `{scenario_configs_file_path}`."
        )

    with open(f"{scenario_configs_dir}/{scenario_name}_scenario.yml") as scenario_config_file:
        settings = yaml.safe_load(scenario_config_file)

    return settings
