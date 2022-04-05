from typing import Optional

from enum import IntEnum
from asterisk_amocrm.infrastructure.event_bus import BaseEvent


__all__ = [
    "CdrDetectionEvent",
]


class CdrDetectionEvent(BaseEvent):

    class Status(IntEnum):
        CANCEL: int = 1
        ANSWER: int = 2
        NO_ANSWER: int = 3
        BUSY: int = 4
        CONGESTION: int = 5
        CHANUNAVAIL: int = 6

    created_at: float
    caller_phone_number: str
    called_phone_number: str
    duration: int
    disposition: Status
    start_timestamp: float
    end_timestamp: float
    unique_id: str
    answer_timestamp: Optional[float] = None
