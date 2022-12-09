from asyncio import AbstractEventLoop
from asyncio import get_running_loop

from typing import Optional

from asterisk_ng.system.configurator import IConfiguratorComponent

from asterisk_ng.system.container import container
from asterisk_ng.system.container import Key
from asterisk_ng.system.container import SingletonResolver

from asterisk_ng.system.plugin_store import PluginStore

from .bootstrap import bootstrap


__all__ = ["Application"]


class Application:

    __slots__ = (
        "__plugin_store",
        "__configurator",
    )

    def __init__(
        self,
        configurator: IConfiguratorComponent,
    ) -> None:
        self.__configurator = configurator
        self.__plugin_store: Optional[PluginStore] = None

    async def handle_startup(self) -> None:
        container.set_resolver(Key(AbstractEventLoop), SingletonResolver(get_running_loop()))

        await self.__configurator.initialize()

        static_configuration = await self.__configurator.get_static_configuration()
        bootstrap(static_configuration)

        self.__plugin_store = container.resolve(Key(PluginStore))
        await self.__plugin_store.initialize()

        plugins_conf = await self.__configurator.get_configuration()
        await self.__plugin_store.set_plugins_settings(plugins_conf.plugins)

    async def handle_shutdown(self) -> None:
        await self.__plugin_store.deinitialize()
        await self.__configurator.deinitialize()
