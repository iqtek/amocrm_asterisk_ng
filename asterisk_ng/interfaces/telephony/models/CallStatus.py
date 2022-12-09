from enum import Enum


__all__ = ["CallStatus"]


class CallStatus(str, Enum):
    ANSWERED: str = "ANSWERED"
    NO_ANSWER: str = "NO_ANSWER"
    BUSY: str = "BUSY"
    FAILED: str = "FAILED"
