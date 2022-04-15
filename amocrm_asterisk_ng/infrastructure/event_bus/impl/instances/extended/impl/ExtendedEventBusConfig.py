from pydantic import BaseModel
from pydantic import PositiveInt


__all__ = [
    "ExtendedEventBusConfig",
]


class ExtendedEventBusConfig(BaseModel):
    workers: PositiveInt = 1
    attempts_left: PositiveInt = 10
