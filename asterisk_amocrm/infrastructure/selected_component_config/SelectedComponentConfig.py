from typing import Any
from typing import Mapping
from typing import Optional

from pydantic import BaseModel


__all__ = [
    "SelectedComponentConfig",
]


class SelectedComponentConfig(BaseModel):
    type: str
    settings: Optional[Mapping[str, Any]] = {}
