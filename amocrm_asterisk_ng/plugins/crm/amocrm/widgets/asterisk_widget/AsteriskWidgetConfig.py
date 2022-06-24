from typing import Dict

from pydantic import BaseModel


__all__ = [
    "AsteriskWidgetConfig",
]


class AsteriskWidgetConfig(BaseModel):

    login: str
    password: str
    users: Dict[str, str]
