from typing import Any
from typing import Mapping

from asterisk_ng.system.plugin import IPlugin
from asterisk_ng.system.plugin import IPluginFactory

from .StandardDomainPlugin import StandardDomainPlugin


__all__ = ["StandardDomainPluginFactory"]


class StandardDomainPluginFactory(IPluginFactory):

    __slots__ = ()

    def __call__(self, settings: Mapping[str, Any]) -> IPlugin:
        return StandardDomainPlugin()
