from typing import Any
from typing import Mapping

from asterisk_ng.system.plugin import IPlugin
from asterisk_ng.system.plugin.core import IPluginFactory

from .RedirectingPlugin import RedirectingPlugin


__all__ = ["RedirectingPluginFactory"]


class RedirectingPluginFactory(IPluginFactory):

    __slots__ = ()

    def __call__(self, settings: Mapping[str, Any]) -> IPlugin:
        return RedirectingPlugin()
