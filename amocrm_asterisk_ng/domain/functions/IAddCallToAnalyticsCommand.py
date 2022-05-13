from typing import Literal

from glassio.dispatcher import ICommand

from ..models import CallStatus


__all__ = [
    "IAddCallToAnalyticsCommand",
]


class IAddCallToAnalyticsCommand(ICommand):

    __slots__ = ()

    async def __call__(
        self,
        unique_id: str,
        phone_number: str,
        direction: Literal["inbound", "outbound"],
        duration: int,
        source: str,
        created_at: int,
        responsible_user_id: int,
        call_status: int,
        call_result: str,
    ) -> None:
        raise NotImplementedError()
