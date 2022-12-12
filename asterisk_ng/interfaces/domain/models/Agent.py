from pydantic import BaseModel

from ...crm_system import CrmUserId


__all__ = ["Agent"]


class Agent(BaseModel):
    user_id: CrmUserId
    phone: str
    name: str
