from typing import Optional

from pydantic import BaseModel

from .CallInfo import CallInfo
from .CallStatus import CallStatus


__all__ = ["AgentStatus"]


class AgentStatus(BaseModel):
    status: CallStatus = CallStatus.NOT_CONVERSATION
    call_info: Optional[CallInfo] = None
