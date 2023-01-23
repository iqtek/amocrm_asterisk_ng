from typing import Any
from typing import Mapping

from .IPlugin import IPlugin


__all__ = ["IPluginFactory"]


class IPluginFactory:

    __slots__ = ()

    def __call__(self, settings: Mapping[str, Any]) -> IPlugin:
        raise NotImplementedError()
