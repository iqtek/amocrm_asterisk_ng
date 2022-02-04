from typing import (
    Mapping,
    Any,
)
from .IAmiManager import IAmiManager


__all__ = [
    "IAmiManagerFactory",
]


class IAmiManagerFactory:

    def get_instance(self, settings: Mapping[str, Any]) -> IAmiManager:
        raise NotImplementedError()
