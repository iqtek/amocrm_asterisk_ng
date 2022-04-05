from typing import Generic
from typing import TypeVar


__all__ = [
    "IConverter",
]


T = TypeVar('T')
S = TypeVar('S')


class IMapper(Generic[T, S]):

    __slots__ = ()

    def convert(self, obj: T) -> S:
        """
        :raise Exception: If a serialization error occurred.
        """
        raise NotImplementedError()

    def deserialize(self, serialized_data: S) -> T:
        """
        :raise Exception: If a deserialization error occurred.
        """
        raise NotImplementedError()
