from pydantic import BaseModel


__all__ = [
    "IEvent",
]


class IEvent(BaseModel):

    class Config:
        allow_mutation = False
