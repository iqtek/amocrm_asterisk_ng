from typing import Any
from typing import Mapping

from pydantic import BaseModel


__all__ = [
    "AmocrmComponentConfig",
]


class AmocrmComponentConfig(BaseModel):
    kernel: Mapping[str, Any]
    widget: Mapping[str, Any]
