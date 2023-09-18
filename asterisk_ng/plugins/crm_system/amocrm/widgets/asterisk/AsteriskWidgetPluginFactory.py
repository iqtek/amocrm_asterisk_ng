from typing import Any
from typing import Mapping

from asterisk_ng.system.plugin import Plugin
from asterisk_ng.system.plugin.core import PluginFactory

from .AsteriskWidgetPlugin import AsteriskWidgetPlugin


__all__ = ["AsteriskWidgetPluginFactory"]


class AsteriskWidgetPluginFactory(IPluginFactory):

    __slots__ = ()

    def __call__(self, settings: Mapping[str, Any]) -> Plugin:
        return AsteriskWidgetPlugin()
