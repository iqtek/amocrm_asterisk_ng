from typing import Optional

from ...core import IState
from ...core import InitializableComponent
from ...core import InitializableComponentException

from ..standard import DeinitializedState
from ..standard import InitializedState
from ..standard import StandardStateFactory
from ..standard import StandardStateMachine


__all__ = [
    "AbstractInitializableComponent",
]


class AbstractInitializableComponent(InitializableComponent):

    __slots__ = (
        "__state_factory",
        "__state_machine",
        "__name",
    )

    def __init__(self, name: Optional[str] = None) -> None:
        self.__name = name or self.__class__.__name__
        self.__state_factory = StandardStateFactory(
            initialize_task=self._initialize,
            deinitialize_task=self._deinitialize,
        )
        self.__state_machine = StandardStateMachine(
            state_factory=self.__state_factory,
        )

    @property
    def state(self) -> IState:
        return self.__state_machine.state

    async def _initialize(self) -> None:
        """Custom initialization code."""
        pass

    async def initialize(self) -> None:
        while True:
            state = self.__state_machine.state
            await state.initialize()

            try:
                self.__state_machine.next()
            except StopIteration as e:
                raise InitializableComponentException() from e
            new_state = self.__state_machine.state

            if issubclass(type(new_state), InitializedState):
                return

    async def deinitialize(self, exception: Optional[Exception] = None) -> None:
        while True:
            state = self.__state_machine.state
            await state.deinitialize()

            try:
                self.__state_machine.next()
            except StopIteration as e:
                raise InitializableComponentException() from e

            new_state = self.__state_machine.state

            if issubclass(type(new_state), DeinitializedState):
                break

        if exception:
            raise exception

    async def _deinitialize(self, exception: Optional[Exception] = None) -> None:
        """Custom deinitialization code."""
        pass

    def __repr__(self) -> str:
        return self.__name
