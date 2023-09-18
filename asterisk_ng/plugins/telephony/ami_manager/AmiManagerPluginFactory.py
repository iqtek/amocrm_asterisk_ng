from typing import Any
from typing import Mapping

from asterisk_ng.system.plugin import Plugin
from asterisk_ng.system.plugin.core import PluginFactory

from .AmiManagerPlugin import AmiManagerPlugin


__all__ = ["AmiManagerPluginFactory"]


class AmiManagerPluginFactory(IPluginFactory):

    __slots__ = ()

    def __call__(self, settings: Mapping[str, Any]) -> Plugin:
        return AmiManagerPlugin()
