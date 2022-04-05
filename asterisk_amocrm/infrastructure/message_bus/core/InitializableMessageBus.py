from abc import ABC

from asterisk_amocrm.infrastructure import InitializableComponent

from .IMessageBus import IMessageBus


__all__ = [
    "InitializableMessageBus",
]


class InitializableMessageBus(IMessageBus, InitializableComponent, ABC):

    __slots__ = ()
