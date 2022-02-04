from abc import ABC
from asterisk_amocrm.infrastructure.component import IComponent
from .IKeyValueStorage import (
    IKeyValueStorage,
)


__all__ = [
    "IKeyValueStorageComponent",
]


class IKeyValueStorageComponent(IComponent, IKeyValueStorage, ABC):
    pass
