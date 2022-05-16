from abc import ABC
from typing import TypeVar

from glassio.mixins import IFactory

from ..utils import ISelectable


__all__ = [
    "ISelectableFactory",
]


T = TypeVar('T')


class ISelectableFactory(IFactory[T], ISelectable, ABC):

    __slots__ = ()
