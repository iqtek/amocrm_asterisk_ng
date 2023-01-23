from typing import Any
from typing import Mapping
from typing import Optional


__all__ = ["IControllerMethod"]


class IControllerMethod:

    __slots__ = ()

    async def __call__(
        self,
        amouser_email: str,
        amouser_id: int,
        **kwargs: Mapping[str, Any]
    ) -> Optional[Any]:
        raise NotImplementedError()
