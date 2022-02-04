from typing import (
    Mapping,
    Generic,
    TypeVar,
    Any
)

from ..core import (
    IFactory,
    IFactoryStore,
)


__all__ = [
    "FactoryStoreImpl",
]


T = TypeVar("T")


class FactoryStoreImpl(IFactoryStore, Generic[T]):

    def __init__(self) -> None:
        self.factories: Dict[str, IFactory[T]] = {}

    def register_factory(self, instance: IFactory[T]) -> None:
        self.factories[instance.type()] = instance

    def get_instance(self, type: str, settings: Mapping[str, Any]) -> T:
        try:
            factory = self.factories[type]
        except KeyError:
            raise KeyError(
                f"Factory type error. There is no such factory: {type}."
            )

        return factory.get_instance(settings)

