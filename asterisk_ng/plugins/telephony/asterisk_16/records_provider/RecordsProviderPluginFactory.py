from typing import Any
from typing import Mapping

from asterisk_ng.system.plugin import IPlugin
from asterisk_ng.system.plugin.core import IPluginFactory

from .RecordsProviderPlugin import RecordsProviderPlugin


__all__ = ["RecordsProviderPluginFactory"]


class RecordsProviderPluginFactory(IPluginFactory):

    __slots__ = ()

    def __call__(self, settings: Mapping[str, Any]) -> IPlugin:
        return RecordsProviderPlugin()
