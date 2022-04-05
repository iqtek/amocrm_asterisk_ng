from abc import ABC
from typing import Any
from typing import Mapping
from typing import TypeVar


from asterisk_amocrm.infrastructure import IFactory, ISelectable


__all__ = [
    "ISelectableFactory",
]


T = TypeVar('T')


class ISelectableFactory(IFactory[T], ISelectable, ABC):

    __slots__ = ()
