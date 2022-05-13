from amocrm_asterisk_ng.infrastructure.event_bus import BaseEvent


__all__ = [
    "RingingEvent",
]


class RingingEvent(BaseEvent):
    """
    Call event.

    Happens when the phone starts ringing. It comes from telephony.
    """
    caller_phone_number: str
    called_phone_number: str
