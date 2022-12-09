from typing import Any
from typing import Mapping

from pydantic import BaseModel


__all__ = ["StaticConfiguration"]


class StaticConfiguration(BaseModel):
    logger: Mapping[str, Any]
