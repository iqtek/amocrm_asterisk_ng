from abc import ABC

from .IEventBus import IEventBus

from asterisk_amocrm.infrastructure import InitializableComponent


__all__ = [
    "InitializableEventBus",
]


class InitializableEventBus(IEventBus, InitializableComponent, ABC):

    __slots__ = ()
