from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .CallDirection import CallDirection
from ...crm_system import CrmUserId
from ...crm_system import CrmContact


__all__ = ["CallDomainModel"]


class CallDomainModel(BaseModel):
    id: str
    agent_id: CrmUserId
    client_phone_number: str
    client_name: Optional[str] = None
    contact: Optional[CrmContact] = None
    direction: CallDirection
    agent_is_mute: bool = False
    created_at: datetime
