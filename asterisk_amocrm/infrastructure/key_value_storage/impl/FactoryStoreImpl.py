from typing import (
    TypeVar,
    Dict,
)
from ..core import (
    IKeyValueStorageFactory,
)


__all__ = [
    "FactoryStoreImpl",
]


class FactoryStoreImpl:

    def __init__(self) -> None:
        self.factories: Dict[str, IKeyValueStorageFactory] = {}

    def register_factory(self, instance: IKeyValueStorageFactory):
        if not isinstance(instance, IKeyValueStorageFactory):
            raise TypeError(
                "Given object does not implement a IKeyValueStorageFactory."
            )
        self.factories[instance.type()] = instance

    def get_instance(self, type: str) -> IKeyValueStorageFactory:
        """
        Returns a storage factory instance that matches the given type.
        :param type: Storage factory string identifier.
        """
        try:
            factory = self.factories[type]
        except KeyError:
            raise KeyError(
                "Storage type error. "
                f"There is no such storage with type={type}"
            )
        return factory
