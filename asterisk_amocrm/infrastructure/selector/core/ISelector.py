from typing import Generic
from typing import TypeVar

from .ISelectable import ISelectable


__all__ = [
    "ISelector",
]


T = TypeVar('T', bound=ISelectable)


class ISelector(Generic[T]):

    __slots__ = ()

    def add_item(self, item: T) -> None:
        raise NotImplementedError()

    def get_item(self, unique_tag: str) -> T:
        """
        :raise KeyError: If there is no item with this tag in the selector.
        """
        raise NotImplementedError()
