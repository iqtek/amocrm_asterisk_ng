import asyncio
import time
from typing import Literal
import re
from asterisk_amocrm.domains import CdrDetectionEvent
from asterisk_amocrm.infrastructure import IDispatcher
from asterisk_amocrm.infrastructure import IEventHandler
from asterisk_amocrm.infrastructure import ILogger

from ..CallLoggingConfig import CallLoggingConfig
from ..commands_handlers import IAddCallToAnalyticsCommand
from ..commands_handlers import IAddCallToUnsortedCommand
from .....core import IGetUserIdByPhoneQuery


__all__ = [
    "CdrDetectionEventHandler",
]


class CdrDetectionEventHandler(IEventHandler):

    __slots__ = (
        "__config",
        "__cdr_endpoint_format_string",
        "__get_user_id_by_phone_query",
        "__add_call_to_analytics_command",
        "__add_call_to_unsorted_command",
        "__logger",
    )

    __CALL_STATUSES = {
        CdrDetectionEvent.Status.CANCEL: 6,
        CdrDetectionEvent.Status.ANSWER: 4,
        CdrDetectionEvent.Status.NO_ANSWER: 6,
        CdrDetectionEvent.Status.BUSY: 7,
        CdrDetectionEvent.Status.CONGESTION: 5,
        CdrDetectionEvent.Status.CHANUNAVAIL: 5,
    }

    def __init__(
        self,
        config: CallLoggingConfig,
        cdr_endpoint_format_string: str,
        add_call_to_analytics_command: IAddCallToAnalyticsCommand,
        add_call_to_unsorted_command: IAddCallToUnsortedCommand,
        get_user_id_by_phone_query: IGetUserIdByPhoneQuery,
        logger: ILogger
    ) -> None:
        self.__config = config
        self.__cdr_endpoint_format_string = cdr_endpoint_format_string
        self.__get_user_id_by_phone_query = get_user_id_by_phone_query
        self.__add_call_to_analytics_command = add_call_to_analytics_command
        self.__add_call_to_unsorted_command = add_call_to_unsorted_command
        self.__logger = logger

    async def __is_internal(self, phone_number: str) -> bool:
        try:
            await self.__get_user_id_by_phone_query(
                phone_number=phone_number
            )
            return True
        except KeyError:
            pass

        pattern = re.compile(self.__config.internal_number_regex)
        match_result = re.match(pattern, phone_number)
        if match_result is not None:
            return True

        return False

    def __make_link(self, unique_id: str):
        base_url = self.__config.base_url.rstrip('/')
        format_str = base_url + self.__cdr_endpoint_format_string
        return format_str.format(unique_id)

    def __get_call_status(self, disposition: CdrDetectionEvent.Status) -> int:

        try:
            return self.__CALL_STATUSES[disposition]
        except ValueError:
            raise ValueError(f"Invalid event disposition {disposition}.")

    async def __get__direction(
        self,
        caller_phone_number: str,
        called_phone_number: str,
    ) -> Literal["inbound", "outbound"]:
        caller_is_internal = await self.__is_internal(caller_phone_number)
        called_is_internal = await self.__is_internal(called_phone_number)
        if caller_is_internal != called_is_internal:
            if caller_is_internal:
                return "outbound"
            else:
                return "inbound"

        elif caller_is_internal:
            self.__logger.info(
                f"CdrDetectionEventHandler: "
                f"Conversation detected between two extensions. "
                f"'{caller_phone_number}' -> '{called_phone_number}'."
            )
        elif called_is_internal:
            self.__logger.info(
                "CdrDetectionEventHandler: "
                f"Unable to determine the direction of the call "
                f"for '{caller_phone_number}' -> '{called_phone_number}'."
            )

        raise Exception()

    async def __call__(self, event: CdrDetectionEvent) -> None:

        try:
            direction = await self.__get__direction(
                caller_phone_number=event.caller_phone_number,
                called_phone_number=event.called_phone_number,
            )
        except Exception:
            self.__logger.warning(
                f"CdrDetectionEventHandler: "
                f"Unable determine direction: "
                f"'{event.caller_phone_number}' -> "
                f"'{event.called_phone_number}'."
            )
            return
        if direction == "outbound":
            internal_phone_number = event.caller_phone_number
            external_phone_number = event.called_phone_number

        else:
            internal_phone_number = event.called_phone_number
            external_phone_number = event.caller_phone_number

        self.__logger.debug(
            f"CdrDetectionEventHandler: "
            f"Call direction: '{direction}' "
            f"internal_phone_number: '{internal_phone_number}' "
            f"external_phone_number: '{external_phone_number}' ."
        )

        responsible_user_id = await self.__get_user_id_by_phone_query(phone_number=internal_phone_number)

        if direction == "outbound" and event.disposition != CdrDetectionEvent.Status.ANSWER:
            # Outgoing unanswered calls are not logged.
            self.__logger.debug(
                "CdrDetectionEventHandler: "
                f"Outgoing unanswered calls are not logged. "
                f"internal_phone_number: '{internal_phone_number}' -> "
                f"external_phone_number: '{external_phone_number}' ."
            )
            return

        await asyncio.sleep(self.__config.postprocessing_delay)

        add_call_to_analytics_exception: Optional[Exception] = None
        try:
            await self.__add_call_to_analytics_command(
                uniq=event.unique_id,
                phone=external_phone_number,
                direction=direction,
                duration=event.duration,
                source=self.__config.source,
                call_status=self.__get_call_status(event.disposition),
                created_at=int(time.time()),
                created_by=responsible_user_id,
                responsible_user_id=responsible_user_id,
                link=self.__make_link(event.unique_id)
            )
            self.__logger.debug(
                "CdrDetectionEventHandler: "
                f"The call with unique_id: '{event.unique_id}' "
                "added to analytics."
            )
            return
        except Exception as e:
            add_call_to_analytics_exception = e

        add_call_to_unsorted_command_exception: Optional[Exception] = None
        try:
            await self.__add_call_to_unsorted_command(
                source_name=self.__config.source,
                source_uid=self.__config.source_uid,
                pipeline_id=self.__config.pipeline_id,
                created_at=int(time.time()),
                uniq=event.unique_id,
                duration=event.duration,
                service_code=self.__config.service_code,
                link=self.__make_link(event.unique_id),
                called=event.called_phone_number,
                caller=event.caller_phone_number,
            )
            self.__logger.debug(
                "CdrDetectionEventHandler: "
                f"The call with unique_id: '{event.unique_id}' "
                "added to unsorted."
            )
            return
        except Exception as e:
            add_call_to_unsorted_command_exception = e

        self.__logger.error(
            "CdrDetectionEventHandler: "
            f"Failed to logging the call with unique_id: '{event.unique_id}'."
        )
        self.__logger.exception(add_call_to_analytics_exception)
        self.__logger.exception(add_call_to_unsorted_command_exception)

        raise Exception(
            "CdrDetectionEventHandler: "
            f"Failed to logging the call with unique_id: '{event.unique_id}'. {add_call_to_analytics_exception}"
        )
