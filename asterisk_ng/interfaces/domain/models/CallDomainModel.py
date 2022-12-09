from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .CallDirection import CallDirection
from ...crm_system import CrmUserId


__all__ = ["CallDomainModel"]


class CallDomainModel(BaseModel):
    id: str
    agent_id: CrmUserId
    client_phone_number: str
    client_name: Optional[str] = None
    direction: CallDirection

    agent_is_mute: bool = False

    created_at: datetime
