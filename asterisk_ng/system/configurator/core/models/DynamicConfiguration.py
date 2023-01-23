from typing import Any
from typing import Mapping

from pydantic import BaseModel


__all__ = ["DynamicConfiguration"]


class DynamicConfiguration(BaseModel):
    plugins: Mapping[str, Any] = {}
