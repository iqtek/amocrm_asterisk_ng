from typing import AbstractSet
from typing import Mapping
from typing import TypeVar


__all__ = [
    "Graph",
]


T = TypeVar('T')


Graph = Mapping[T, AbstractSet[T]]
