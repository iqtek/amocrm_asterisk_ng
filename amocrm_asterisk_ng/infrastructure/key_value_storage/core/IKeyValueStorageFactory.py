from typing import Optional

from .InitializableKeyValueStorage import InitializableKeyValueStorage


__all__ = [
    "IKeyValueStorageFactory",
]


class IKeyValueStorageFactory:

    __slots__ = ()

    def get_instance(
        self,
        prefix: Optional[str] = None
    ) -> InitializableKeyValueStorage:
        """
        Returns an instance IKeyValueStorageComponent.

        :param prefix : The string prefix is added to the
            beginning of the key to avoid naming conflicts.
        """
        raise NotImplementedError()
