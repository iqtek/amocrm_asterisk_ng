from typing import Any
from typing import Mapping

from asterisk_ng.system.plugin import IPlugin
from asterisk_ng.system.plugin.core import IPluginFactory

from .AmiManagerPlugin import AmiManagerPlugin


__all__ = ["AmiManagerPluginFactory"]


class AmiManagerPluginFactory(IPluginFactory):

    __slots__ = ()

    def __call__(self, settings: Mapping[str, Any]) -> IPlugin:
        return AmiManagerPlugin()
