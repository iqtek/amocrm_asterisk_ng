from typing import Optional
from datetime import datetime
from enum import IntEnum
from asterisk_amocrm.infrastructure.event_bus import IEvent


__all__ = [
    "CdrDetectionEvent",
]


class CdrDetectionEvent(IEvent):

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
    start_time: datetime
    end_time: datetime
    unique_id: str
    answer_time: Optional[datetime] = None
