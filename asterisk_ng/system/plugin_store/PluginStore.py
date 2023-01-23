from typing import Any
from typing import Mapping
from typing import MutableMapping
from typing import Optional

from asterisk_ng.system.components import AbstractInitializableComponent

from asterisk_ng.system.logger import ILogger
from asterisk_ng.system.plugin import IPlugin
from asterisk_ng.system.plugin import IPluginFactory

from .PluginStoreConfig import PluginStoreConfig


__all__ = ["PluginStore"]


class PluginStore(AbstractInitializableComponent):

    __slots__ = (
        "__plugins_factories",
        "__uploaded_plugins",
        "__old_config",
        "__logger",
    )

    def __init__(
        self,
        plugins_factories: MutableMapping[str, IPluginFactory],
        logger: ILogger,
    ) -> None:
        super().__init__("PluginStore")
        self.__plugins_factories = plugins_factories
        self.__logger = logger

        self.__uploaded_plugins: MutableMapping[str, Optional[IPlugin]] = {}
        self.__old_config: Optional[PluginStoreConfig] = None

    async def _initialize(self) -> None:
        pass

    async def set_plugins_settings(self, settings: Mapping[str, Any]) -> None:
        await self.__logger.info(f"New plugin settings have been received.")

        config = PluginStoreConfig(**settings)

        for plugin_name in config.uploaded:
            factory = self.__plugins_factories[plugin_name]
            settings = config.plugins_settings.get(plugin_name) or {}
            plugin = factory({})  # hardcode

            try:
                await plugin.upload(settings)
            except Exception as exc:
                await self.__logger.critical(f"Error of uploading: <{plugin_name}>.", exc)
                raise exc

            await self.__logger.info(f"Plugin <{plugin_name}> success uploaded.")
            self.__uploaded_plugins[plugin_name] = plugin

        await self.__logger.info(f"Settings plugins are updated.")

    async def _deinitialize(self, exception: Optional[Exception] = None) -> None:
        for plugin_name, plugin in reversed(self.__uploaded_plugins.items()):
            try:
                await plugin.unload()
            except Exception as exc:
                await self.__logger.error(f"Error of unloading plugin: <{plugin_name}>.", exc)
            await self.__logger.info(f"Plugin <{plugin_name}> success unloaded.")
