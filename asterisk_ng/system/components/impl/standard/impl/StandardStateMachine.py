from ....core import IState

from ..core import CreatedState
from ..core import DeinitializedState
from ..core import DeinitializingState
from ..core import IStateFactory
from ..core import IStateMachine
from ..core import InitializedState
from ..core import InitializingState


__all__ = [
    "StandardStateMachine",
]


class StandardStateMachine(IStateMachine):

    __slots__ = (
        "__state",
        "__state_factory",
        "__state_graph",
    )

    def __init__(
        self,
        state_factory: IStateFactory,
    ) -> None:
        self.__state_factory = state_factory
        self.__state = self.__state_factory.get_instance(CreatedState)
        self.__state_graph = {
            CreatedState: InitializingState,
            InitializingState: InitializedState,
            InitializedState: DeinitializingState,
            DeinitializingState: DeinitializedState,
            DeinitializedState: InitializingState,
        }

    @property
    def state(self) -> IState:
        return self.__state

    def next(self) -> None:
        try:
            next_state = self.__state_graph[type(self.__state)]
        except KeyError:
            raise StopIteration(
                f"Unknown next state after: {type(self.__state)}."
            )
        self.__state = self.__state_factory.get_instance(next_state)
