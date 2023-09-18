from typing import Any
from typing import Mapping

from asterisk_ng.system.plugin import Plugin
from asterisk_ng.system.plugin import IPluginFactory

from .AmoClientPlugin import AmoClientPlugin


__all__ = ["AmoClientPluginFactory"]


class AmoClientPluginFactory(IPluginFactory):

    __slots__ = ()

    def __call__(self, settings: Mapping[str, Any]) -> Plugin:
        return AmoClientPlugin()
