from typing import Any
from typing import Mapping

from asterisk_ng.system.plugin import Plugin
from asterisk_ng.system.plugin.core import PluginFactory

from .RecordsProviderPlugin import RecordsProviderPlugin


__all__ = ["RecordsProviderPluginFactory"]


class RecordsProviderPluginFactory(IPluginFactory):

    __slots__ = ()

    def __call__(self, settings: Mapping[str, Any]) -> Plugin:
        return RecordsProviderPlugin()
