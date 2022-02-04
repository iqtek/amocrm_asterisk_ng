from typing import (
    Optional,
    Mapping,
    Union,
    Any,
)
from pydantic import (
    BaseModel
)
from .instances import (
    RedisStorageConfigModel,
)


__all__ = [
    "KeyValueStorageConfigModel",
]


class KeyValueStorageConfigModel(BaseModel):

    type: Optional[str] = "redis"
    storage_config: Optional[RedisStorageConfigModel] = None
