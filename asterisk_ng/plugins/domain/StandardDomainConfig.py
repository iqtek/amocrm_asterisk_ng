from typing import Literal
from typing import Mapping
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

from pydantic import BaseModel


__all__ = ["StandardDomainConfig"]


class StandardDomainConfig(BaseModel):
    agents: Mapping[str, str]  # Mapping[email, phone]
    redirect_responsible_agent: Optional[str] = None  # email
    client_corrector: Optional[Sequence[Tuple[str, str]]] = None

    call_responsible_strategy: Sequence[Union[Literal['by_entity'], Literal['default'], Literal['last_active']]] = ["default"]
    default_responsible_agent: str
