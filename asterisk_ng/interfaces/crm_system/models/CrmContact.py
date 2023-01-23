from typing import Optional

from pydantic import BaseModel

from .CrmUserId import CrmUserId


__all__ = ["CrmContact"]


class CrmContact(BaseModel):
    id: int
    name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    responsible_user_id: Optional[CrmUserId] = None
