from typing import Type
from typing import TypeVar


__all__ = [
    "Ioc",
]


T = TypeVar('T')


class Ioc:

    __slots__ = ()

    def get_instance(self, key: Type[T]) -> T:
        """
        Get an instance by the type of its parent class.

        :raise KeyError: If
        """
        raise NotImplementedError()

    def set_instance(self, key: Type[T], instance: T) -> None:
        """
        Set an instance by the type of its parent class.

        :raise TypeError: The passed instance does not inherit
            from the key class.
        """
        raise NotImplementedError()
