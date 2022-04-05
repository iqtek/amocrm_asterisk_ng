from typing import Any
from typing import Mapping

from pydantic import BaseModel


__all__ = [
    "AmocrmKernelComponentConfig",
]


class AmocrmKernelComponentConfig(BaseModel):
    integration: Mapping[str, Any]
    call_logging: Mapping[str, Any]
