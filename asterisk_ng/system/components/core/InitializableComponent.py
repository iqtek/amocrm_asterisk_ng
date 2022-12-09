from typing import Optional

from .IState import IState


__all__ = [
    "InitializableComponent",
]


class InitializableComponent:

    __slots__ = ()

    @property
    def state(self) -> IState:
        """Get current state."""
        raise NotImplementedError()

    async def initialize(self) -> None:
        """
        Initialize the component.

        :raise InitializableComponentException.
        """
        raise NotImplementedError()

    async def deinitialize(self, exception: Optional[Exception] = None) -> None:
        """
        Deinitialize the component.

        When the component is deinitialized,
        the specified exception will be thrown.

        :raise InitializableComponentException.
        """
        raise NotImplementedError()
