from typing import Any
from typing import Mapping

from asterisk_ng.system.plugin import Plugin
from asterisk_ng.system.plugin.core import PluginFactory

from .Asterisk16FunctionPlugin import Asterisk16FunctionPlugin


__all__ = ["Asterisk16FunctionPluginFactory"]


class Asterisk16FunctionPluginFactory(IPluginFactory):

    __slots__ = ()

    def __call__(self, settings: Mapping[str, Any]) -> Plugin:
        return Asterisk16FunctionPlugin()
