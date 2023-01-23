from datetime import datetime
from typing import Optional

from asterisk_ng.system.event_bus import BaseEvent

from ..models import CallStatus


__all__ = [
    "CallCompletedTelephonyEvent",
]


class CallCompletedTelephonyEvent(BaseEvent):
    unique_id: str
    caller_phone_number: str
    called_phone_number: str
    created_at: datetime
