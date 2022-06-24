from pydantic import BaseModel


__all__ = [
    "ConversationProperties",
]


class ConversationProperties(BaseModel):
    unique_id: str
    contact_name: str
    contact_phone: str
    is_enabled_hold: bool = False
    is_mute: bool = False
    timestamp: int
