from typing import (
    Mapping,
    Generic,
    TypeVar,
    Any,
)


__all__ = [
    "IFactory",
]


T = TypeVar("T")


class IFactory(Generic[T]):

    @classmethod
    def type(cls) -> str:
        """
        Return unique string ID of the factory.
        :return: unique string
        """
        raise NotImplementedError()

    def get_instance(self, settings: Mapping[str, Any]) -> T:
        raise NotImplementedError()
