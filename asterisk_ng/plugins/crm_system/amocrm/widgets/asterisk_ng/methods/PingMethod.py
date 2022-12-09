from typing import Optional
from typing import Mapping
from typing import Any

from ..controller import IControllerMethod


__all__ = ["PingMethod"]


class PingMethod(IControllerMethod):

    __slots__ = ()

    async def __call__(
        self,
        amouser_email: str,
        amouser_id: int,
        **kwargs,
    ) -> Optional[Mapping[str, Any]]:
        return {"ping": "pong"}
