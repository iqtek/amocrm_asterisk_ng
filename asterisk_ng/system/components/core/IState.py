from typing import Optional


__all__ = [
    "IState",
]


class IState:

    __slots__ = ()

    async def initialize(self) -> None:
        """
        Delegate initialization to state.

        :raise InitializableComponentException.
        """
        raise NotImplementedError()

    async def deinitialize(self, exception: Optional[Exception] = None) -> None:
        """
        Delegate deinitialization to state.

        :raise InitializableComponentException.
        """
        raise NotImplementedError()
