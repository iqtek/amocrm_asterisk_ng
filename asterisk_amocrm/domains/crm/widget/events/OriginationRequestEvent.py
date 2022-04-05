from asterisk_amocrm.infrastructure.event_bus import BaseEvent


__all__ = [
    "OriginationRequestEvent",
]


class OriginationRequestEvent(BaseEvent):

    caller_phone_number: str
    called_phone_number: str
