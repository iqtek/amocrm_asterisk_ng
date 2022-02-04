from typing import Any, Mapping

from pydantic import BaseModel


__all__ = [
    "Asterisk16Config",
]


class Asterisk16Config(BaseModel):
    ami: Mapping[str, Any]
    cdr: Mapping[str, Any]
    dial: Mapping[str, Any]
