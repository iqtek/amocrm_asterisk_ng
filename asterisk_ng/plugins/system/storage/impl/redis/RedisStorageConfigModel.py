from typing import Optional

from pydantic import BaseModel
from pydantic import Field


__all__ = ["RedisStorageConfigModel"]


class RedisStorageConfigModel(BaseModel):
    host: str = "127.0.0.1"
    port: int = Field(6379, gt=0, lt=65536)
    database: Optional[int] = 1
    password: Optional[str] = None
