from typing import Mapping, Any
import os
from asterisk_ng.system.container import Key
from asterisk_ng.system.container import SingletonResolver
from asterisk_ng.system.container import container

from .impl import FileConverterImpl
from .core import IFileConverter

from asterisk_ng.system.plugin import Plugin
from asterisk_ng.system.plugin import Interface
from asterisk_ng.system.plugin import PluginInterface

from .FileConverterPluginConfig import FileConverterPluginConfig


__all__ = ["FileConverterPlugin"]


class FileConverterPlugin(Plugin[PluginInterface]):

    __slots__ = ()

    def __init__(self) -> None:
        pass

    @property
    def interface(self) -> PluginInterface:
        return PluginInterface(
            exported=Interface(
                container=[Key(IFileConverter)],
            )
        )

    async def upload(self, settings: Mapping[str, Any]) -> None:
        os.makedirs(settings["tmp_dir"], exist_ok=True)

        config = FileConverterPluginConfig(**settings)

        converter = FileConverterImpl(str(config.tmp_dir))
        container.set_resolver(Key(IFileConverter), SingletonResolver(converter))

    async def reload(self, settings: Mapping[str, Any]) -> None:
        config = FileConverterPluginConfig(**settings)
        converter = FileConverterImpl(str(config.tmp_dir))
        container.set_resolver(Key(IFileConverter), SingletonResolver(converter))

    async def unload(self) -> None:
        container.delete_resolver(Key(IFileConverter))
