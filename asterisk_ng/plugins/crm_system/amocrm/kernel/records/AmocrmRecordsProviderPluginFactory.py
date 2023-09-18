from typing import Any
from typing import Mapping

from asterisk_ng.system.plugin import Plugin
from asterisk_ng.system.plugin import IPluginFactory

from .AmocrmRecordsProviderPlugin import AmocrmRecordsProviderPlugin


__all__ = ["AmocrmRecordsProviderPluginFactory"]


class AmocrmRecordsProviderPluginFactory(IPluginFactory):

    __slots__ = ()

    def __call__(self, settings: Mapping[str, Any]) -> Plugin:
        return AmocrmRecordsProviderPlugin()
