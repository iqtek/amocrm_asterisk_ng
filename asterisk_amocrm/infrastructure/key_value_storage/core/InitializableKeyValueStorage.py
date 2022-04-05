from abc import ABC

from asterisk_amocrm.infrastructure import InitializableComponent

from .IKeyValueStorage import IKeyValueStorage


__all__ = [
    "InitializableKeyValueStorage",
]


class InitializableKeyValueStorage(InitializableComponent, IKeyValueStorage, ABC):

    __slots__ = ()
