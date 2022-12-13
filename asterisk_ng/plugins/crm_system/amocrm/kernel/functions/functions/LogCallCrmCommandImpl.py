from time import time
from typing import Tuple

from amocrm_api_client import AmoCrmApiClient
from amocrm_api_client.make_amocrm_request import IncorrectDataException
from amocrm_api_client.models.call import AddCall
from amocrm_api_client.models.unsorted import UnsortedCall
from amocrm_api_client.models.unsorted import UnsortedCallMetadata

from asterisk_ng.interfaces import CrmCallDirection
from asterisk_ng.interfaces import CrmCallResult
from asterisk_ng.interfaces import CrmUserId
from asterisk_ng.interfaces import ILogCallCrmCommand

from asterisk_ng.plugins.crm_system.amocrm.kernel.records import IGenerateLinkFunction

from ..AmocrmFunctionsPluginConfig import AmocrmFunctionsPluginConfig


__all__ = ["LogCallCrmCommandImpl"]


class LogCallCrmCommandImpl(ILogCallCrmCommand):

    __slots__ = (
        "__config",
        "__amo_client",
        "__generate_link_function",
        "__pipeline_id",
    )

    def __init__(
        self,
        config: AmocrmFunctionsPluginConfig,
        amo_client: AmoCrmApiClient,
        generate_link_function: IGenerateLinkFunction,
        pipeline_id: int,
    ) -> None:
        self.__config = config
        self.__amo_client = amo_client
        self.__generate_link_function = generate_link_function
        self.__pipeline_id = pipeline_id

    def __get_amocrm_call_result(self, result: CrmCallResult) -> Tuple[int, str]:
        RESULTS_MAPPING = {
            CrmCallResult.ANSWERED: (4, "Разговор состоялся."),
            CrmCallResult.NO_ANSWER: (6, "Не дозвонился."),
            CrmCallResult.BUSY: (7, "Номер занят."),
            CrmCallResult.INVALID_NUMBER: (5, "Неверный номер."),
        }
        return RESULTS_MAPPING[result]

    async def __call__(
        self,
        unique_id: str,
        internal_phone_number: str,
        external_phone_number: str,
        direction: CrmCallDirection,
        call_result: CrmCallResult,
        responsible_user_id: CrmUserId,
        duration: int,
    ) -> None:
        link = await self.__generate_link_function(unique_id)
        timestamp = int(time())

        amocrm_str_direction = "inbound" if direction == CrmCallDirection.INBOUND else "outbound"
        amocrm_call_result = self.__get_amocrm_call_result(call_result)

        call = AddCall(
            uniq=unique_id,
            direction=amocrm_str_direction, # noqa
            duration=duration,
            source=self.__config.source,
            link=link,
            phone=external_phone_number,
            call_result=amocrm_call_result[1],
            call_status=amocrm_call_result[0],
            responsible_user_id=responsible_user_id.id,
            created_at=timestamp,
        )

        try:
            await self.__amo_client.calls.add(call)
        except IncorrectDataException:
            pass

        if direction != CrmCallDirection.INBOUND:
            return

        metadata = UnsortedCallMetadata(
            uniq=unique_id,
            from_=external_phone_number,
            phone=internal_phone_number,
            called_at=timestamp,
            duration=duration,
            link=link,
            service_code=self.__config.service_code,
            is_call_event_needed=True,
        )

        call = UnsortedCall(
            source_uid=self.__config.source_uid,
            source_name=self.__config.source_name,
            pipeline_id=self.__pipeline_id,
            created_at=timestamp,
            metadata=metadata,
        )

        await self.__amo_client.unsorted.add_call(call)
