from datetime import datetime

from asterisk_ng.system.event_bus import BaseEvent


__all__ = ["CallCreatedTelephonyEvent"]


class CallCreatedTelephonyEvent(BaseEvent):
    unique_id: str
    caller_phone_number: str
    called_phone_number: str
    created_at: datetime
