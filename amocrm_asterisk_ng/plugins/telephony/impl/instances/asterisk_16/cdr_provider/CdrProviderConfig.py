from typing import Mapping
from typing import Any

from pydantic import BaseModel


__all__ = [
    "CdrProviderConfig",
]


class CdrProviderConfig(BaseModel):

    mysql: Mapping[str, Any]
    media_root: str = "/var/spool/asterisk/monitor/%Y/%m/%d/"
