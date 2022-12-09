from asterisk_ng.system.components import InitializableComponent

from .IConfigurator import IConfigurator


__all__ = ["IConfiguratorComponent"]


class IConfiguratorComponent(IConfigurator, InitializableComponent):

    __slots__ = ()
