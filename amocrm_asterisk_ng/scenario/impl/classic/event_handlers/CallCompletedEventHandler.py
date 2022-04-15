from time import time

from amocrm_asterisk_ng.domain import CallCompletedEvent
from amocrm_asterisk_ng.domain import CallStatus
from amocrm_asterisk_ng.domain import ICrm

from ..functions import IGetCallDirectionFunction


__all__ = [
    "CallCompletedEventHandler",
]


class CallCompletedEventHandler(IEventHandler):

    __slots__ = (
        "__crm",
        "__get_call_direction_function",
    )

    def __init__(self, crm: ICrm, get_call_direction_function: IGetCallDirectionFunction) -> None:
        self.__crm = crm
        self.__get_call_direction_function = get_call_direction_function

    async def __call__(self, event: CallCompletedEvent) -> None:

        time_now = int(time())

        direction = self.__get_call_direction_function(
            caller_phone_number=event.caller_phone_number,
            called_phone_number=event.called_phone_number,
        )
        if direction == "inbound":
            internal_phone_number = event.called_phone_number
            external_phone_number = event.caller_phone_number

        else:
            internal_phone_number = event.caller_phone_number
            external_phone_number = event.called_phone_number

        if direction == "outbound" and event.disposition != CallStatus.ANSWER:
            # Outgoing unanswered calls are not logged.
            return

        responsible_user_id = await self.__crm.get_user_id_by_phone(phone_number=internal_phone_number)

        await asyncio.sleep(self.__config.postprocessing_delay)

        await self.__crm.add_call_to_analytics(
            unique_id=event.unique_id,
            phone_number=external_phone_number,
            direction=direction,
            duration=event.duration,
            source=self.__config.source,
            created_at=time_now,
            responsible_user_id=responsible_user_id,
            call_status=event.disposition,
        )

        pipeline_id = await self.__crm.get_pipeline_id_py_name(
            pipeline_name=self.__config.pipeline_name
        )

        await self.__crm.add_call_to_unsorted(
            unique_id=event.unique_id,
            caller_phone_number=event.caller_phone_number,
            called_phone_number=event.called_phone_number,
            duration=event.duration,
            source_name=self.__config.source_name,
            source_uid=self.__config.source_uid,
            service_code=self.__config.service_code,
            pipeline_id=pipeline_id,
            created_at=time_now,
        )
