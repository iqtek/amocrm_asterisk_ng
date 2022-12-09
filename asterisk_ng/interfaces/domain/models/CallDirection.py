from enum import Enum


__all__ = ["CallDirection"]


class CallDirection(Enum):
    INBOUND = "INBOUND"
    OUTBOUND = "OUTBOUND"
    INTERNAL = "INTERNAL"
