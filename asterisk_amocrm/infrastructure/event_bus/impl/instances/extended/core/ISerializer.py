from typing import Generic
from typing import TypeVar


__all__ = [
    "ISerializer",
]


T = TypeVar('T')
S = TypeVar('S')


class ISerializer(Generic[T, S]):

    __slots__ = ()

    def serialize(self, obj: T) -> S:
        """
        :raise Exception: If a serialization error occurred.
        """
        raise NotImplementedError()

    def deserialize(self, serialized_data: S) -> T:
        """
        :raise Exception: If a deserialization error occurred.
        """
        raise NotImplementedError()
