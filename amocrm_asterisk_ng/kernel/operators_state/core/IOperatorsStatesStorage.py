from .OperatorState import OperatorState


__all__ = [
    "IOperatorsStatesStorage",
]


class IOperatorsStatesStorage:
    """
    The global state of all operators present in the system.
    """

    __slots__ = ()

    async def set_state(self, amouser_id: int, state: UserState) -> None:
        raise NotImplementedError()

    async def get_state(self, amouser_id: int) -> OperatorState:
        raise NotImplementedError()

    async def get_state_difference(self, amouser_id: int, timeout: float = 10) -> OperatorState:
        raise NotImplementedError()

    async def delete_state(self, amouser_id: int) -> None:
        raise NotImplementedError()
