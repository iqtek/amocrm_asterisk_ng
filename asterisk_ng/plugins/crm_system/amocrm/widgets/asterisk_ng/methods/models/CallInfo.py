from typing import Optional

from pydantic import BaseModel


__all__ = ["CallInfo"]


class CallInfo(BaseModel):
    unique_id: str
    contact_name: Optional[str] = None
    contact_phone: str
    is_hold: bool
    is_mute: bool
    timestamp: int
