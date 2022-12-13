from typing import Mapping
from typing import Optional
from typing import Sequence
from typing import Tuple

from pydantic import BaseModel


__all__ = ["StandardDomainConfig"]


class StandardDomainConfig(BaseModel):
    agents: Mapping[str, str]  # Mapping[email, phone]
    responsible_agent: Optional[str] = None  # email
    client_corrector: Optional[Sequence[Tuple[str, str]]] = None
