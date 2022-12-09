from typing import Any
from typing import Mapping

from asterisk_ng.system.plugin import IPlugin
from asterisk_ng.system.plugin import IPluginFactory

from .ReflectorPlugin import ReflectorPlugin


__all__ = ["ReflectorPluginFactory"]


class ReflectorPluginFactory(IPluginFactory):

    __slots__ = ()

    def __call__(self, settings: Mapping[str, Any]) -> IPlugin:
        return ReflectorPlugin()
