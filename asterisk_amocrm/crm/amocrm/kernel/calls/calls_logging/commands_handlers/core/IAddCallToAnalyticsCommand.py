from typing import Literal
from typing import Optional

from asterisk_amocrm.infrastructure import ICommand


__all__ = [
    "IAddCallToAnalyticsCommand",
]


class IAddCallToAnalyticsCommand(ICommand):

    __slots__ = ()

    async def __call__(
        self,
        phone: str,
        direction: Literal["inbound", "outbound"],
        duration: int,
        source: str,
        created_at: int,
        responsible_user_id: int,
        call_status: Optional[int] = None,
        call_result: Optional[str] = None,
        created_by: Optional[int] = None,
        updated_at: Optional[int] = None,
        updated_by: Optional[int] = None,
        uniq: Optional[str] = None,
        link: Optional[str] = None,
    ) -> None:
        raise NotImplementedError()
