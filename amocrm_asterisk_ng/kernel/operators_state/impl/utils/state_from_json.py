from ...core import OperatorState


__all__ = [
    "state_from_json",
]


def state_from_json(json: str) -> OperatorState:
    return OperatorState.parse_raw(json)
