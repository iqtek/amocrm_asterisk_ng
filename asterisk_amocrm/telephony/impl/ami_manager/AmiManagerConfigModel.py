from pydantic import (
    BaseModel,
    Field,
)


__all__ = [
    "AmiManagerConfigModel",
]


class AmiManagerConfigModel(BaseModel):

    host: str = "127.0.0.1"
    port: int = Field(5038, gt=0, lt=65536)
    user: str
    secret: str
