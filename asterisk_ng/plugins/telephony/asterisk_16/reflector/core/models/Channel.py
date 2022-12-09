from pydantic import BaseModel


__all__ = [
    "Channel",
]


class Channel(BaseModel):
    name: str
    unique_id: str
    linked_id: str
    state: str
