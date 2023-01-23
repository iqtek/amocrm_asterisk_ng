from pydantic import BaseModel
from pydantic import Field


__all__ = ["MySqlConfig"]


class MySqlConfig(BaseModel):
    user: str
    password: str
    host: str = "127.0.0.1"
    port: int = Field(3306, gt=0, lt=65536)
    database: str = "asteriskcdrdb"
