from abc import ABC

from asterisk_ng.system.components import InitializableComponent

from .IAmiManager import IAmiManager


class IAmiManagerComponent(InitializableComponent, IAmiManager, ABC):

    __slots__ = ()
