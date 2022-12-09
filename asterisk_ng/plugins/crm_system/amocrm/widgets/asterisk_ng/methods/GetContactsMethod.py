from typing import Any
from typing import Mapping
from typing import Optional

from asterisk_ng.interfaces import CrmUserId
from asterisk_ng.interfaces import IHangupDomainCommand
from .models import Contact

from ..controller import IControllerMethod


__all__ = ["GetContactsMethod"]


class GetContactsMethod(IControllerMethod):

    __slots__ = ()

    async def __call__(
        self,
        amouser_email: str,
        amouser_id: int,
        start_with: Optional[str] = None,
        max_results: int = 100,
    ) -> Any:
        return []
