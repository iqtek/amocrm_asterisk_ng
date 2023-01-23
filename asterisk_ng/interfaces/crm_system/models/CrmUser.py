from pydantic import BaseModel

from .CrmUserId import CrmUserId


__all__ = ["CrmUser"]


class CrmUser(BaseModel):
    id: CrmUserId
    name: str
