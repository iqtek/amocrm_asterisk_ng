from typing import Mapping
from typing import Optional

from pydantic import BaseModel


__all__ = ["StandardDomainConfig"]


class StandardDomainConfig(BaseModel):
    agents: Mapping[str, str]  # Mapping[email, phone]
    responsible_agent: Optional[str] = None  # email
