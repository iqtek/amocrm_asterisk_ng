from typing import Any
from typing import Mapping
from typing import Optional

from ..controller import IControllerMethod
from ..controller import InvalidParamsException

from asterisk_ng.interfaces import CrmUserId


__all__ = ["SetHoldMethod"]


class SetHoldMethod(IControllerMethod):

    __slots__ = ()

    async def __call__(
        self,
        amouser_email: str,
        amouser_id: int,
        is_hold: Optional[bool] = None
    ) -> Optional[Mapping[str, Any]]:
        raise NotImplementedError()
