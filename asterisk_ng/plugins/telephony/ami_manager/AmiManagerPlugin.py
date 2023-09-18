from asyncio import AbstractEventLoop
from typing import Any
from typing import Mapping
from typing import Optional

from asterisk_ng.system.logger import ILogger

from asterisk_ng.system.container import Key
from asterisk_ng.system.container import SingletonResolver
from asterisk_ng.system.container import container

from asterisk_ng.system.plugin import Plugin
from asterisk_ng.system.plugin import Interface
from asterisk_ng.system.plugin import PluginInterface

from .core import IAmiManager
from .core import IAmiManagerComponent
from .impl import AmiManagerComponentFactory


__all__ = ["AmiManagerPlugin"]


class AmiManagerPlugin(Plugin[PluginInterface]):

    __slots__ = (
        "__ami_manager_component",
        "__ami_manager_component_factory"
    )

    @property
    def interface(self) -> PluginInterface:
        return PluginInterface(
            imported=Interface(
                container=[
                    Key(AbstractEventLoop),
                    Key(ILogger)
                ],
            ),
            exported=Interface(
                container=[
                    Key(IAmiManager)
                ],
            )
        )

    def __init__(self) -> None:
        self.__ami_manager_component_factory: Optional[AmiManagerComponentFactory] = None
        self.__ami_manager_component: Optional[IAmiManagerComponent] = None

    async def upload(self, settings: Mapping[str, Any]) -> None:

        event_loop = container.resolve(Key(AbstractEventLoop))
        logger = container.resolve(Key(ILogger))

        self.__ami_manager_component_factory = AmiManagerComponentFactory(
            event_loop=event_loop,
            logger=logger,
        )

        self.__ami_manager_component = self.__ami_manager_component_factory(settings=settings)
        await self.__ami_manager_component.initialize()
        container.set_resolver(Key(IAmiManager), SingletonResolver(self.__ami_manager_component))

    async def reload(self, settings: Mapping[str, Any]) -> None:
        new_ami_manager_component = self.__ami_manager_component_factory(settings=settings)
        await new_ami_manager_component.initialize()
        container.set_resolver(Key(IAmiManager), SingletonResolver(new_ami_manager_component))
        await self.__ami_manager_component.deinitialize()
        self.__ami_manager_component = new_ami_manager_component

    async def unload(self) -> None:
        container.delete_resolver(Key(IAmiManager))
        await self.__ami_manager_component.deinitialize()
