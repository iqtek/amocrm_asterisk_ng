from typing import Any
from typing import Mapping

from pydantic import BaseModel
from pydantic import Field


__all__ = [
    "IntegrationConfig",
    "ServerConfig",
]


class InfrastructureConfig(BaseModel):
    storage: Mapping[str, Any]
    logger: Mapping[str, Any]


class IntegrationConfig(BaseModel):
    scenario: str = "classic"
    scenario_configs_dir = "./configs"
    crm: Mapping[str, Any]
    telephony: Mapping[str, Any]

    infrastructure: InfrastructureConfig
