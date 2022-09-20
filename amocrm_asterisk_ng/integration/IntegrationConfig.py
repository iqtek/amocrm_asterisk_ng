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
    scenario: Mapping[str, Any]
    crm: Mapping[str, Any]
    telephony: Mapping[str, Any]

    infrastructure: InfrastructureConfig
