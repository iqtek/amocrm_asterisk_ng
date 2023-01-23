from pydantic import BaseModel


__all__ = ["AsteriskNgConfig"]


class AsteriskNgConfig(BaseModel):
    secret_key: str = "AsteriskNG"
