from typing import Any
from typing import Mapping

from pydantic import BaseModel


__all__ = [
    "Asterisk16Config",
]


class Asterisk16Config(BaseModel):
    storage_prefix: str = "telephony"
    ami: Mapping[str, Any]
    cdr: Mapping[str, Any]
    dial: Mapping[str, Any]
