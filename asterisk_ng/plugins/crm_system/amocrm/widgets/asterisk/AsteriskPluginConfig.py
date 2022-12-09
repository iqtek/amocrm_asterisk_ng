from typing import Mapping

from pydantic import BaseModel


__all__ = ["AsteriskPluginConfig"]


class AsteriskPluginConfig(BaseModel):
    login: str
    password: str
