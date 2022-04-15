from abc import ABC

from .IEventBus import IEventBus

from amocrm_asterisk_ng.infrastructure import InitializableComponent


__all__ = [
    "InitializableEventBus",
]


class InitializableEventBus(IEventBus, InitializableComponent, ABC):

    __slots__ = ()
