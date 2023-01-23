from pydantic import BaseModel
from pydantic import Field


__all__ = ["FastapiPluginConfig"]


class FastapiPluginConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = Field(8000, gt=0, lt=65536)
    workers: int = 1
