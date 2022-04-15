from amo_crm_api_client import AmoCrmApiClient
from amo_crm_api_client.exceptions import AmocrmClientException

from amocrm_asterisk_ng.infrastructure import ILogger
from ..core import IAddCallToUnsortedCommand


__all__ = [
    "AddCallToUnsortedCommand",
]


class AddCallToUnsortedCommand(IAddCallToUnsortedCommand):

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
        source_name: str,
        source_uid: str,
        pipeline_id: int,
        created_at: int,
        uniq: str,
        duration: int,
        service_code: str,
        link: str,
        called: str,
        caller: str,
    ) -> None:

        await self.__amo_client.unsorted.add_call(
            uniq=uniq,
            caller=caller,
            called=called,
            duration=duration,
            source_name=source_name,
            source_uid=source_uid,
            service_code=service_code,
            created_at=created_at,
            pipeline_id=pipeline_id,
            link=link,
        )
