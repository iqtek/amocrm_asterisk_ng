from datetime import datetime

from asterisk_ng.system.event_bus import BaseEvent


__all__ = ["MuteStatusUpdateTelephonyEvent"]


class MuteStatusUpdateTelephonyEvent(BaseEvent):
    phone: str
    is_mute: bool
    created_at: datetime
