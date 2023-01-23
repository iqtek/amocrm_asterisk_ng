from pydantic import BaseModel
from pydantic import Field


__all__ = ["AmiManagerConfig"]


class AmiManagerConfig(BaseModel):
    user: str = "admin"
    secret: str
    host: str = "127.0.0.1"
    port: int = Field(5038, gt=0, lt=65536)
