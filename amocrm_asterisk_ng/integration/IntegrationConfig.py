from typing import Any
from typing import Mapping

from pydantic import BaseModel
from pydantic import Field


__all__ = [
    "IntegrationConfig",
    "ServerConfig",
]


class ServerConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = Field(8080, gt=0, lt=65536)


class InfrastructureConfig(BaseModel):
    integration: ServerConfig
    message_bus: Mapping[str, Any]
    event_bus: Mapping[str, Any]
    storage: Mapping[str, Any]
    logger: Mapping[str, Any]


class IntegrationConfig(BaseModel):
    scenario: str = "classic"
    scenario_configs_dir = "configs"
    crm: Mapping[str, Any]
    telephony: Mapping[str, Any]

    infrastructure: InfrastructureConfig
