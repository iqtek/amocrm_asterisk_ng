from typing import Generic
from typing import TypeVar
from typing import MutableMapping

from ..core import ISelector
from ..core import ISelectable


__all__ = [
    "SelectorImpl",
]


T = TypeVar("T", bound=ISelectable)


class SelectorImpl(ISelector[T]):

    __slots__ = (
        "__items",
    )

    def __init__(self) -> None:
        self.__items: MutableMapping[str, T] = {}

    def add_item(self, item: T) -> None:
        self.__items[item.unique_tag()] = item

    def get_item(self, unique_tag: str) -> T:
        try:
            return self.__items[unique_tag]
        except KeyError:
            raise KeyError(
                f"There is no item with this tag: '{unique_tag}'."
            )
