from enum import Enum


__all__ = ["CallStatus"]


class CallStatus(str, Enum):
    CONVERSATION: str = "CONVERSATION",
    NOT_CONVERSATION: str = "NOT_CONVERSATION"
