from ...core import OperatorState


__all__ = [
    "state_to_json",
]


def state_to_json(state: OperatorState) -> str:
    return state.json()
