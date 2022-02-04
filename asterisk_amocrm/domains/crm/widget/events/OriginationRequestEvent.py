from asterisk_amocrm.infrastructure.event_bus import IEvent


__all__ = [
    "OriginationRequestEvent",
]


class OriginationRequestEvent(IEvent):

    caller_phone_number: str
    called_phone_number: str
