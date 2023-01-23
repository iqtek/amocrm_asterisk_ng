from typing import Any
from typing import Mapping

from pydantic import BaseModel


__all__ = [
    "Headers",
    "Command",
]


class Headers(BaseModel):
    amouser_email: str
    amouser_id: int
    widget_version: str


class Command(BaseModel):
    jsonrpc: str
    id: int
    method: str
    params: Mapping[str, Any] = {}
