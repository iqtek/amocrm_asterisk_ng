from datetime import datetime
from typing import Optional
from asterisk_ng.system.event_bus import BaseEvent
from ..models import CallStatus


__all__ = ["CallReportReadyTelephonyEvent"]


class CallReportReadyTelephonyEvent(BaseEvent):
    unique_id: str

    caller_phone_number: str
    called_phone_number: str

    duration: int
    disposition: CallStatus

    call_start_at: datetime
    call_end_at: datetime
    answer_at: Optional[datetime] = None

    created_at: datetime
