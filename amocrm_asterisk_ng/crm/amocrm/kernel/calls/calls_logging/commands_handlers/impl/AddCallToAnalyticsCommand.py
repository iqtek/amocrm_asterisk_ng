from typing import Literal
from typing import Optional

from amo_crm_api_client import AmoCrmApiClient
from amo_crm_api_client.exceptions import AmocrmClientException

from amocrm_asterisk_ng.infrastructure import ILogger
from ..core import IAddCallToAnalyticsCommand


__all__ = [
    "AddCallToAnalyticsCommand",
]


class AddCallToAnalyticsCommand(IAddCallToAnalyticsCommand):

    __slots__ = (
        "__amo_client",
        "__logger",
    )

    def __init__(
        self,
        amo_client: AmoCrmApiClient,
        logger: ILogger,
    ) -> None:
        self.__amo_client = amo_client
        self.__logger = logger

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

        await self.__amo_client.calls.add(
            uniq=uniq,
            phone=phone,
            direction=direction,
            duration=duration,
            source=source,
            call_status=call_status,
            created_at=created_at,
            responsible_user_id=responsible_user_id,
            call_result=call_result,
            created_by=created_by,
            updated_at=updated_at,
            updated_by=updated_by,
            link=link,
        )
