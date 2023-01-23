from typing import Any
from typing import Mapping
from typing import Sequence

from pydantic import BaseModel


__all__ = ["PluginStoreConfig"]


class PluginStoreConfig(BaseModel):
    uploaded: Sequence[str] = []
    plugins_settings: Mapping[str, Mapping[str, Any]] = {}
