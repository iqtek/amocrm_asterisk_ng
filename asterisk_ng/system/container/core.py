from typing import Any
from typing import Generic
from typing import Optional
from typing import Type
from typing import TypeVar


__all__ = [
    "Key",
    "IResolver"
]


T = TypeVar('T')


class Key(Generic[T]):

    __slots__ = (
        "__obj_type",
        "__label",
    )

    def __init__(
        self,
        obj_type: Type[T],
        label: Optional[Any] = None
    ) -> None:
        self.__obj_type = obj_type
        self.__label = label

    @property
    def obj_type(self) -> Type[T]:
        return self.__obj_type

    @property
    def label(self) -> Optional[Any]:
        return self.__label

    def __eq__(self, other: 'Key') -> bool:
        return self is other or (
                self.__obj_type is other.obj_type and self.__label is other.__label)

    def __hash__(self) -> int:
        return hash((self.__obj_type, self.__label))

    def __repr__(self) -> str:
        return f"Key(obj_type: `{self.__obj_type}`, label: `{self.__label}`)"


class IResolver(Generic[T]):

    __slots__ = ()

    def __call__(self, needy: Optional[Any] = None) -> T:
        raise NotImplementedError()
