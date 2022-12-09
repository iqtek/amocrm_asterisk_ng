from datetime import datetime

from asterisk_ng.system.event_bus import BaseEvent


__all__ = ["HoldStatusUpdateTelephonyEvent"]


class HoldStatusUpdateTelephonyEvent(BaseEvent):
    phone: str
    is_hold: bool
    created_at: datetime
