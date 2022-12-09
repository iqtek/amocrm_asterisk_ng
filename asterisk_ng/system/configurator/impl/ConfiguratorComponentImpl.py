import os
from typing import Optional

from yaml import dump
from yaml import safe_load

from asterisk_ng.system.components import AbstractInitializableComponent

from .ConfigFileModel import ConfigFileModel
from .ConfiguratorConfig import ConfiguratorConfig

from ..core import DynamicConfiguration
from ..core import IConfiguratorComponent
from ..core import StaticConfiguration


__all__ = ["ConfiguratorComponentImpl"]


class ConfiguratorComponentImpl(IConfiguratorComponent, AbstractInitializableComponent):

    __slots__ = (
        "__config",
        "__config_file",
    )

    def __init__(self, config: ConfiguratorConfig) -> None:
        super().__init__(name="Configurator")
        self.__config = config
        self.__config_file: Optional[ConfigFileModel] = None

    def __load__configuration(self, filepath: str) -> None:
        with open(filepath, "r") as config_file:
            settings = safe_load(config_file) or {}
            self.__config_file = ConfigFileModel(**settings)

    async def _initialize(self) -> None:

        if os.path.isfile(self.__config.saved_config_path):
            try:
                return self.__load__configuration(self.__config.saved_config_path)
            except Exception:
                pass
        if os.path.isfile(self.__config.config_path):
            self.__load__configuration(self.__config.config_path)
        else:
            raise Exception("Configuration file not found.")

    async def get_static_configuration(self) -> StaticConfiguration:
        return self.__config_file.static

    async def set_configuration(self, configuration: DynamicConfiguration) -> None:
        self.__config_file.dynamic = configuration

    async def get_configuration(self) -> DynamicConfiguration:
        return self.__config_file.dynamic

    async def _deinitialize(self, exception: Optional[Exception] = None) -> None:
        if not self.__config.enable_saving:
            return

        with open(self.__config.saved_config_path, "w") as config_file:
            dump(self.__config_file.dict(), stream=config_file)
