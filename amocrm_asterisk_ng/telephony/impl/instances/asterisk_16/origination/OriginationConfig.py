from pydantic import BaseModel


__all__ = [
    "OriginationConfig",
]


class OriginationConfig(BaseModel):
    context: str = "from-internal"
    timeout: int = 30000
