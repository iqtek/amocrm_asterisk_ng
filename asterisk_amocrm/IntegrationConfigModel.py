from pydantic import (
    IPvAnyAddress,
    BaseModel,
    Field,
)


__all__ = [
    "IntegrationConfigModel",
]


class IntegrationConfigModel(BaseModel):
    host: str = "0.0.0.0"
    port: int = Field(8080, gt=0, lt=65536)
