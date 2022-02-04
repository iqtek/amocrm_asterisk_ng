from typing import (
    Mapping,
    Generic,
    TypeVar,
    Any,
)
from .IFactory import IFactory


__all__ = [
    "IFactoryStore"
]


T = TypeVar("T")


class IFactoryStore(Generic[T]):

    def register_factory(self, instance: IFactory[T]) -> None:
        raise NotImplementedError()

    def get_instance(
        self,
        type: str,
        settings: Mapping[str, Any]
    ) -> T:
        """
        :raise KeyError: If factory with given type is not registered.
        """
        raise NotImplementedError()
