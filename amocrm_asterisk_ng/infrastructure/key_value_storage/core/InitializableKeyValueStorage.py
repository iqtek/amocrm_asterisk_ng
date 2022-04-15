from abc import ABC

from amocrm_asterisk_ng.infrastructure import InitializableComponent

from .IKeyValueStorage import IKeyValueStorage


__all__ = [
    "InitializableKeyValueStorage",
]


class InitializableKeyValueStorage(InitializableComponent, IKeyValueStorage, ABC):

    __slots__ = ()
