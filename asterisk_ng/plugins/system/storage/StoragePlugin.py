from typing import Any
from typing import Mapping
from typing import Optional

from asterisk_ng.system.components import InitializableComponent
from asterisk_ng.system.logger import ILogger

from asterisk_ng.system.container import Key
from asterisk_ng.system.container import container
from asterisk_ng.system.plugin import IPlugin
from asterisk_ng.system.plugin import Interface
from asterisk_ng.system.plugin import PluginInterface

from .core import IKeyValueStorage
from .impl import RedisKeyValueStorageFactory

from .StorageResolver import StorageResolver


__all__ = ["StoragePlugin"]


class StoragePlugin(IPlugin[PluginInterface]):

    __slots__ = (
        "__logger",
        "__storage_factory",
    )

    def __init__(self) -> None:
        self.__logger: Optional[ILogger] = None
        self.__storage_factory: Optional[InitializableComponent] = None

    @property
    def interface(self) -> PluginInterface:
        return PluginInterface(
            imported=Interface(
              container=[Key(ILogger)]
            ),
            exported=Interface(
                container=[Key(IKeyValueStorage)],
            )
        )

    async def upload(self, settings: Mapping[str, Any]) -> None:
        self.__logger = container.resolve(Key(ILogger), needy="StoragePlugin")

        self.__storage_factory = RedisKeyValueStorageFactory(settings=settings, logger=self.__logger)
        await self.__storage_factory.initialize()
        resolver = StorageResolver(self.__storage_factory)
        container.set_resolver(Key(IKeyValueStorage), resolver)

    async def reload(self, settings: Mapping[str, Any]) -> None:
        new_storage_factory = RedisKeyValueStorageFactory(settings=settings, logger=self.__logger)
        await new_storage_factory.initialize()
        resolver = StorageResolver(new_storage_factory)
        container.set_resolver(Key(IKeyValueStorage), resolver)
        self.__storage_factory = new_storage_factory

    async def unload(self) -> None:
        container.delete_resolver(Key(IKeyValueStorage))
        await self.__storage_factory.deinitialize()
