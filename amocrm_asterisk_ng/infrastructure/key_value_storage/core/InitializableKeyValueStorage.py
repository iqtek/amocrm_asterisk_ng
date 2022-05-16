from abc import ABC

from glassio.initializable_components import InitializableComponent

from .IKeyValueStorage import IKeyValueStorage


__all__ = [
    "InitializableKeyValueStorage",
]


class InitializableKeyValueStorage(InitializableComponent, IKeyValueStorage, ABC):

    __slots__ = ()
