from pydantic import BaseModel, Field


__all__ = [
    "MySqlConfigModel",
]


class MySqlConfigModel(BaseModel):

    host: str = "127.0.0.1"
    port: int = Field(3306, gt=0, lt=65536)
    database: str = "asteriskcdrdb"
    user: str
    password: str
