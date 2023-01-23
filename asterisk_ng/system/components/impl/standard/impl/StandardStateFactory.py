from typing import Any
from typing import Callable
from typing import Coroutine
from typing import Type

from ....core import IState

from ..core import DeinitializingState
from ..core import IStateFactory
from ..core import InitializingState


__all__ = [
    "StandardStateFactory",
]


class StandardStateFactory(IStateFactory):

    __slots__ = (
        "__initialize_task",
        "__deinitialize_task",
    )

    def __init__(
        self,
        initialize_task: Callable[[], Coroutine[Any, Any, None]],
        deinitialize_task: Callable[[], Coroutine[Any, Any, None]],
    ) -> None:
        self.__initialize_task = initialize_task
        self.__deinitialize_task = deinitialize_task

    def get_instance(self, state_type: Type[IState]) -> IState:
        if issubclass(state_type, InitializingState):
            return InitializingState(
                self.__initialize_task,
            )
        if issubclass(state_type, DeinitializingState):
            return DeinitializingState(
                self.__deinitialize_task,
            )

        return state_type()
