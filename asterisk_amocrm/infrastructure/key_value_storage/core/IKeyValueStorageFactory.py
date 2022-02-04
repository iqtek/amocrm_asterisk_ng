from typing import Optional
from .IKeyValueStorageComponent import IKeyValueStorageComponent


__all__ = [
    "IKeyValueStorageFactory",
]


class IKeyValueStorageFactory:

    @classmethod
    def type(cls) -> str:
        """
        Returns the string identifier of the storage type.
        :return: String identifier of the storage type.
        """
        raise NotImplementedError()

    def get_instance(self, prefix: Optional[str] = None) -> IKeyValueStorageComponent:
        """
        Returns an instance IKeyValueStorageComponent.
        :param prefix : The string prefix is added to the
        beginning of the key to avoid naming conflicts.
        :return: Instance IKeyValueStorageComponent.
        """
        raise NotImplementedError()
