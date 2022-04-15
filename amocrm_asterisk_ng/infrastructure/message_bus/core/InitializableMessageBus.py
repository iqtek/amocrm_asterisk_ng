from abc import ABC

from amocrm_asterisk_ng.infrastructure import InitializableComponent

from .IMessageBus import IMessageBus


__all__ = [
    "InitializableMessageBus",
]


class InitializableMessageBus(IMessageBus, InitializableComponent, ABC):

    __slots__ = ()
