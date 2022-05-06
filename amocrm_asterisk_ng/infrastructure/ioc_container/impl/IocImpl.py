from typing import Any
from typing import MutableMapping
from typing import Type
from typing import TypeVar

from ..core import Ioc


__all__ = [
    "IocImpl",
]


T = TypeVar('T')


class IocImpl(Ioc):

    __slots__ = (
        "__dictionary",
        "__instances",
    )

    def __init__(self) -> None:
        self.__dictionary: MutableMapping[str, Any] ={}
        self.__instances: MutableMapping[Type[T], T] = {}

    def set(self, key: str, value: Any) -> None:
        self.__dictionary[key] = value

    def get(self, key: str) -> Any:
        return self.__dictionary[key]

    def get_instance(self, key: Type[T]) -> T:
        try:
            return self.__instances[key]
        except KeyError:
            raise KeyError(
                f"Instance of type '{key}' not found."
            )

    def set_instance(self, key: Type[T], instance: T) -> None:
        if not isinstance(instance, key):
            raise TypeError(
                "The specified instance is not a subtype of the key."
            )
        self.__instances[key] = instance
