from abc import ABC
from typing import Any
from typing import Mapping
from typing import TypeVar


from amocrm_asterisk_ng.infrastructure import IFactory, ISelectable


__all__ = [
    "ISelectableFactory",
]


T = TypeVar('T')


class ISelectableFactory(IFactory[T], ISelectable, ABC):

    __slots__ = ()
