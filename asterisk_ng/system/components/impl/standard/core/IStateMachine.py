from ....core import IState


__all__ = [
    "IStateMachine",
]


class IStateMachine:
    """
    Component state machine.

    Stores a state graph and navigates through it.
    """

    __slots__ = ()

    @property
    def state(self) -> IState:
        """Get current state."""
        raise NotImplementedError()

    def next(self) -> IState:
        """
        Move the state machine to the next state.

        :raise StopIteration: If the next state is not defined.
        """
        raise NotImplementedError()
