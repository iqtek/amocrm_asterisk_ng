from typing import Any
from typing import Mapping

from asterisk_ng.system.plugin import IPlugin
from asterisk_ng.system.plugin.core import IPluginFactory

from .Asterisk16FunctionPlugin import Asterisk16FunctionPlugin


__all__ = ["Asterisk16FunctionPluginFactory"]


class Asterisk16FunctionPluginFactory(IPluginFactory):

    __slots__ = ()

    def __call__(self, settings: Mapping[str, Any]) -> IPlugin:
        return Asterisk16FunctionPlugin()
