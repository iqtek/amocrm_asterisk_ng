from typing import List
from pydantic import BaseModel


__all__ = [
    "Call"
]


class Call(BaseModel):
    linked_id: str
    channels_unique_ids: List[str] = []
