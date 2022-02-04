from pydantic import BaseModel


__all__ = [
    "OriginationConfig",
]


class OriginationConfig(BaseModel):
    context: str
    timeout: int = 30000
