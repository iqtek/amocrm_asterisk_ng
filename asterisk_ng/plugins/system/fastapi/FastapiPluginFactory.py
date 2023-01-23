from typing import Any
from typing import Mapping

from asterisk_ng.system.plugin import IPlugin
from asterisk_ng.system.plugin import IPluginFactory

from .FastapiPlugin import FastapiPlugin


__all__ = ["FastapiPluginFactory"]


class FastapiPluginFactory(IPluginFactory):

    __slots__ = ()

    def __call__(self, settings: Mapping[str, Any]) -> IPlugin:
        return FastapiPlugin()
