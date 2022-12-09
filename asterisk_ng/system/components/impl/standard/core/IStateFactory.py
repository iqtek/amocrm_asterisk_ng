from typing import Type
from typing import TypeVar

from ....core import IState


__all__ = [
    "IStateFactory",
]


T = TypeVar('T', bound=IState)


class IStateFactory:

    """Creates a state of the given type."""

    __slots__ = ()

    def get_instance(self, state_type: Type[T]) -> T:
        """Instantiate the state."""
        raise NotImplementedError()
