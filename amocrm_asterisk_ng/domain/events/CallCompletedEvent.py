from typing import Optional

from amocrm_asterisk_ng.infrastructure.event_bus import BaseEvent

from ..models import CallStatus


__all__ = [
    "CallCompletedEvent",
]


class CallCompletedEvent(BaseEvent):

    unique_id: str
    created_at: float

    caller_phone_number: str
    called_phone_number: str

    duration: int

    disposition: CallStatus

    start_timestamp: float
    end_timestamp: float
    answer_timestamp: Optional[float] = None
