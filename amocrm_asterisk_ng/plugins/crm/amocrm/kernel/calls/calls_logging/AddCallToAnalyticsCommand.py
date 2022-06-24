from typing import Literal

from amocrm_api_client import AmoCrmApiClient
from amocrm_api_client.make_amocrm_request import IncorrectDataException
from amocrm_api_client.models.call import AddCall
from glassio.logger import ILogger

from amocrm_asterisk_ng.domain import EntityWithThisNumberNotExistException
from amocrm_asterisk_ng.domain import IAddCallToAnalyticsCommand
from .MakeLinkFunction import IMakeLinkFunction


__all__ = [
    "AddCallToAnalyticsCommand",
]


class AddCallToAnalyticsCommand(IAddCallToAnalyticsCommand):

    __slots__ = (
        "__amo_client",
        "__make_link_function",
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
        call_result: str,
    ) -> None:

        link = await self.__make_link_function(unique_id)

        call = AddCall(
            uniq=unique_id,
            direction=direction,
            duration=duration,
            source=source,
            link=link,
            phone=phone_number,
            call_result=call_result,
            call_status=call_status,
            responsible_user_id=responsible_user_id,
            created_at=created_at,
        )
        try:
            await self.__amo_client.calls.add(call)
        except IncorrectDataException:
            raise EntityWithThisNumberNotExistException()
