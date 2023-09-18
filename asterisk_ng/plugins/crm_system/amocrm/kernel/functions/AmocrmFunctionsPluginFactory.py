from typing import Any
from typing import Mapping

from asterisk_ng.system.plugin import Plugin
from asterisk_ng.system.plugin import IPluginFactory

from .AmocrmFunctionsPlugin import AmocrmFunctionsPlugin


__all__ = ["AmocrmFunctionsPluginFactory"]


class AmocrmFunctionsPluginFactory(IPluginFactory):

    __slots__ = ()

    def __call__(self, settings: Mapping[str, Any]) -> Plugin:
        return AmocrmFunctionsPlugin()
