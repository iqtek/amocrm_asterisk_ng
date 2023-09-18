from typing import Any
from typing import Mapping

from asterisk_ng.system.plugin import Plugin
from asterisk_ng.system.plugin import IPluginFactory

from .ViaAuthorizerTokenProviderPlugin import AmoClientPlugin


__all__ = ["ViaAuthorizerTokenProviderPluginFactory"]


class ViaAuthorizerTokenProviderPluginFactory(IPluginFactory):

    __slots__ = ()

    def __call__(self, settings: Mapping[str, Any]) -> Plugin:
        return AmoClientPlugin()
