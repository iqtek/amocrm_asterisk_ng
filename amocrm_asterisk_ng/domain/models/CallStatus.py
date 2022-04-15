from enum import IntEnum


__all__ = [
    "CallStatus",
]


class CallStatus(IntEnum):
    CANCEL: int = 1
    ANSWER: int = 2
    NO_ANSWER: int = 3
    BUSY: int = 4
    CONGESTION: int = 5
    CHANUNAVAIL: int = 6
