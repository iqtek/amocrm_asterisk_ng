from typing import Any
from typing import Callable
from typing import Coroutine
from typing import Optional

from ....core import IState
from ....core import InitializableComponentException


__all__ = [
    "CreatedState",
    "InitializingState",
    "InitializedState",
    "DeinitializingState",
    "DeinitializedState",
]


class CreatedState(IState):

    async def initialize(self) -> None:
        pass

    async def deinitialize(self, exception: Optional[Exception] = None) -> None:
        raise InitializableComponentException(
            "The component has not yet been initialized."
        )


class InitializingState(IState):

    __slots__ = (
        "__initialize_task",
    )

    def __init__(
        self,
        initialize_task: Callable[[], Coroutine[Any, Any, None]]
    ) -> None:
        self.__initialize_task = initialize_task

    async def initialize(self) -> None:
        await self.__initialize_task()

    async def deinitialize(self, exception: Optional[Exception] = None) -> None:
        raise InitializableComponentException(
            "Component is initializing now."
        ) from exception


class InitializedState(IState):

    __slots__ = ()

    async def initialize(self) -> None:
        raise InitializableComponentException(
            "Component already initialized."
        )

    async def deinitialize(self, exception: Optional[Exception] = None) -> None:
        pass


class DeinitializingState(IState):

    __slots__ = (
        "__deinitialize_task",
    )

    def __init__(self, deinitialize_task: Callable[[], Coroutine[Any, Any, None]]) -> None:
        self.__deinitialize_task = deinitialize_task

    async def initialize(self) -> None:
        raise InitializableComponentException(f"Component is deinitializing now.")

    async def deinitialize(self, exception: Optional[Exception] = None) -> None:
        await self.__deinitialize_task()


class DeinitializedState(IState):

    async def initialize(self) -> None:
        pass

    async def deinitialize(self, exception: Optional[Exception] = None) -> None:
        raise InitializableComponentException(
            "Component already deinitialized."
        ) from exception
