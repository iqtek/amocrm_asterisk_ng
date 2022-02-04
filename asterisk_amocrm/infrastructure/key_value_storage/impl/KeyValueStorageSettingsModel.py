from typing import (
    Optional,
    Mapping,
    Any,
)
from pydantic import (
    BaseModel
)


__all__ = [
    "KeyValueStorageSettingsModel",
]


class KeyValueStorageSettingsModel(BaseModel):

    type: Optional[str] = "redis"
    storage_settings: Optional[Mapping[str, Any]]
