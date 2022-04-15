from typing import Any
from typing import Mapping

from ...core import IEvent


__all__ = [
    "to_mapping",
]


def to_mapping(event: IEvent) -> Mapping[str, Any]:
    return event.dict()
