from enum import Enum


__all__ = ["CrmCallResult"]


class CrmCallResult(Enum):
    ANSWERED = "ANSWERED"
    NO_ANSWER = "NO_ANSWER"
    BUSY = "BUSY"
    INVALID_NUMBER = "INVALID_NUMBER"
