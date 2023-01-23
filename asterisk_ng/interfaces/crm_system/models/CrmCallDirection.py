from enum import Enum


__all__ = ["CrmCallDirection"]


class CrmCallDirection(Enum):
    INBOUND = "INBOUND"
    OUTBOUND = "OUTBOUND"
