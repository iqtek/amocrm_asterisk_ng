from typing import Any
from typing import Optional

from asterisk_ng.system.container import IResolver
from asterisk_ng.plugins.system.storage import IKeyValueStorage
from asterisk_ng.plugins.system.storage import IKeyValueStorageFactory


__all__ = ["StorageResolver"]


class StorageResolver(IResolver):

    __slots__ = (
        "__storage_factory",
        "__storage_counter",
    )

    def __init__(
        self,
        storage_factory: IKeyValueStorageFactory,
    ) -> None:
        self.__storage_factory = storage_factory
        self.__storage_counter: int = 0

    def __call__(self, needy: Optional[Any] = None) -> IKeyValueStorage:
        if needy is not None:
            return self.__storage_factory(prefix=needy)

        storage = self.__storage_factory(prefix=str(self.__storage_counter))
        self.__storage_counter += 1
        return storage
