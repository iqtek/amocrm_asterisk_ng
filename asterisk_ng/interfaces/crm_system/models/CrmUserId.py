from typing import Optional

from pydantic import BaseModel


__all__ = ["CrmUserId"]


class CrmUserId(BaseModel):
    id: int
    email: Optional[str] = None

    def __hash__(self):
        return hash((type(self), self.id))

    def __eq__(self, other):
        if type(other) is type(self):
            return self.id == other.id
        else:
            return False
