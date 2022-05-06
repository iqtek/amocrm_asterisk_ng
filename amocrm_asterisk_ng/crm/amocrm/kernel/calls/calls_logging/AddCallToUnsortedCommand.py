from typing import MutableMapping

from amocrm_api_client import AmoCrmApiClient
from amocrm_api_client.models.unsorted import UnsortedCall
from amocrm_api_client.models.unsorted import UnsortedCallMetadata

from amocrm_asterisk_ng.domain import IAddCallToUnsortedCommand
from amocrm_asterisk_ng.infrastructure import ILogger
from .MakeLinkFunction import IMakeLinkFunction


__all__ = [
    "AddCallToUnsortedCommand",
]


class AddCallToUnsortedCommand(IAddCallToUnsortedCommand):

    __slots__ = (
        "__amo_client",
        "__make_link_function",
        "__pipelines",
        "__logger",
    )

    def __init__(
        self,
        amo_client: AmoCrmApiClient,
        make_link_function: IMakeLinkFunction,
        logger: ILogger,
    ) -> None:
        self.__amo_client = amo_client
        self.__make_link_function = make_link_function
        self.__pipelines: MutableMapping[str, int] = {}
        self.__logger = logger

    async def __call__(
        self,
        unique_id: str,
        caller_phone_number: str,
        called_phone_number: str,
        duration: int,
        source_name: str,
        source_uid: str,
        service_code: str,
        pipeline_name: str,
        created_at: int,
    ) -> None:

        if pipeline_name not in self.__pipelines.keys():
            pipelines = await self.__amo_client.pipelines.get_all()
            for pipeline in pipelines:
                self.__pipelines[pipeline.name] = pipeline.id

        pipeline_id = self.__pipelines[pipeline_name]

        link = await self.__make_link_function(unique_id)

        metadata = UnsortedCallMetadata(
            uniq=unique_id,
            from_=caller_phone_number,
            phone=called_phone_number,
            called_at=created_at,
            duration=duration,
            link=link,
            service_code=service_code,
            is_call_event_needed=True,
        )
        call = UnsortedCall(
            source_uid=source_uid,
            source_name=source_name,
            pipeline_id=pipeline_id,
            created_at=created_at,
            metadata=metadata,
        )

        await self.__amo_client.unsorted.add_call(call)
