from typing import Literal
from typing import Optional

from amo_crm_api_client import AmoCrmApiClient
from amo_crm_api_client.exceptions import AmocrmClientException

from amocrm_asterisk_ng.infrastructure import ILogger
from amocrm_asterisk_ng.domain import IAddCallToAnalyticsCommand


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
        unique_id: str,
        phone_number: str,
        direction: Literal["inbound", "outbound"],
        duration: int,
        source: str,
        created_at: int,
        responsible_user_id: int,
        call_status: int,
    ) -> None:

        await self.__amo_client.calls.add(
            uniq=unique_id,
            phone=phone_number,
            direction=direction,
            duration=duration,
            source=source,
            call_status=call_status,
            created_at=created_at,
            responsible_user_id=responsible_user_id,
            call_result=call_result,
            link=link,
        )
