import asyncio
from time import time

from glassio.event_bus import IEventHandler

from amocrm_asterisk_ng.domain import CallCompletedEvent
from amocrm_asterisk_ng.domain import CallStatus
from amocrm_asterisk_ng.domain import IAddCallToAnalyticsCommand
from amocrm_asterisk_ng.domain import IAddCallToUnsortedCommand
from amocrm_asterisk_ng.domain import IGetUserIdByPhoneQuery
from amocrm_asterisk_ng.domain import EntityWithThisNumberNotExistException

from ..ClassicScenarioConfig import CallCompletedEventHandlerConfig
from ..functions import IGetCallDirectionFunction
from ..functions import INormalizePhoneFunction

__all__ = [
    "CallCompletedEventHandler",
]


class CallCompletedEventHandler(IEventHandler):

    __slots__ = (
        "__config",
        "__add_call_to_analytics_command",
        "__add_call_to_unsorted_command",
        "__get_user_id_by_phone_query",
        "__get_call_direction_function",
        "__normalize_phone_function",
    )

    def __init__(
        self,
        config: CallCompletedEventHandlerConfig,
        add_call_to_analytics_command: IAddCallToAnalyticsCommand,
        add_call_to_unsorted_command: IAddCallToUnsortedCommand,
        get_user_id_by_phone_query: IGetUserIdByPhoneQuery,
        get_call_direction_function: IGetCallDirectionFunction,
        normalize_phone_function: INormalizePhoneFunction,
    ) -> None:
        self.__config = config
        self.__add_call_to_analytics_command = add_call_to_analytics_command
        self.__add_call_to_unsorted_command = add_call_to_unsorted_command
        self.__get_user_id_by_phone_query = get_user_id_by_phone_query
        self.__get_call_direction_function = get_call_direction_function
        self.__normalize_phone_function = normalize_phone_function

    def __get_call_status(self, call_status: CallStatus) -> int:

        __CALL_STATUSES = {
            CallStatus.CANCEL: 6,
            CallStatus.ANSWER: 4,
            CallStatus.NO_ANSWER: 6,
            CallStatus.BUSY: 7,
            CallStatus.CONGESTION: 5,
            CallStatus.CHANUNAVAIL: 5,
        }

        try:
            return __CALL_STATUSES[call_status]
        except ValueError:
            raise ValueError(f"Invalid event call_status {disposition}.")

    async def __call__(self, event: CallCompletedEvent) -> None:

        time_now = int(time())

        try:
            direction = await self.__get_call_direction_function(
                caller_phone_number=event.caller_phone_number,
                called_phone_number=event.called_phone_number,
            )
        except Exception:
            return
        if direction == "inbound":
            internal_phone_number = event.called_phone_number
            external_phone_number = event.caller_phone_number

        else:
            internal_phone_number = event.caller_phone_number
            external_phone_number = event.called_phone_number

        if direction == "outbound" and event.disposition != CallStatus.ANSWER:
            # Outgoing unanswered calls are not logged.
            return

        responsible_user_id = await self.__get_user_id_by_phone_query(phone_number=internal_phone_number)

        await asyncio.sleep(self.__config.postprocessing_delay)
        external_phone_number = await self.__normalize_phone_function(external_phone_number)
        try:
            await self.__add_call_to_analytics_command(
                unique_id=event.unique_id,
                phone_number=external_phone_number,
                direction=direction,
                duration=event.duration,
                source=self.__config.source,
                created_at=time_now,
                responsible_user_id=responsible_user_id,
                call_status=self.__get_call_status(event.disposition),
                call_result="",
            )
            return
        except EntityWithThisNumberNotExistException:
            pass

        await self.__add_call_to_unsorted_command(
            unique_id=event.unique_id,
            caller_phone_number=event.caller_phone_number,
            called_phone_number=event.called_phone_number,
            duration=event.duration,
            source_name=self.__config.source_name,
            source_uid=self.__config.source_uid,
            service_code=self.__config.service_code,
            pipeline_name=self.__config.pipeline_name,
            created_at=time_now,
        )
        return
