from abc import ABC

from pydantic import BaseModel

from ...core import IEvent


__all__ = [
    "BaseEvent",
]


class BaseEvent(BaseModel, IEvent, ABC):
    pass
