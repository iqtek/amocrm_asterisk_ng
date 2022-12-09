from typing import Any
from typing import Mapping

from ..models import PluginInterface
from ...core import IPlugin


__all__ = ["AbstractPlugin"]


class AbstractPlugin(IPlugin[PluginInterface]):

    __slots__ = ()

    @property
    def interface(self) -> PluginInterface:
        return PluginInterface()

    async def upload(self, settings: Mapping[str, Any]) -> None:
        pass

    async def reload(self, settings: Mapping[str, Any]) -> None:
        await self.unload()
        await self.upload(settings)

    async def unload(self) -> None:
        pass
