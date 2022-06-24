from enum import Enum


__all__ = [
    "OperatorStatus",
]


class OperatorStatus(Enum):
    """
    The current status of the operator.
    """
    TALKING: 'OperatorStatus' = "TALKING"
    NOT_TALKING: 'OperatorStatus' = "NOT_TALKING"
    DISABLED: 'OperatorStatus' = "DISABLED"
