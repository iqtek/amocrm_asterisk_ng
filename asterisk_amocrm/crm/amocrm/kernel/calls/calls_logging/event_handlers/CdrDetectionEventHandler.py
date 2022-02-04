import asyncio
import time
from typing import Literal

from asterisk_amocrm.domains import CdrDetectionEvent
from asterisk_amocrm.infrastructure import IDispatcher, IEventHandler, ILogger
from ..CallLoggingConfig import CallLoggingConfig
from ..commands import AddCallToAnalyticsCommand, AddCallToUnsortedCommand
from .....core import GetUserIdByPhoneQuery


__all__ = [
    "CdrDetectionEventHandler",
]


class CdrDetectionEventHandler(IEventHandler):

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
        dispatcher: IDispatcher,
        logger: ILogger
    ) -> None:
        self.__config = config
        self.__dispatcher = dispatcher
        self.__logger = logger

    async def __is_internal(self, phone_number: str) -> bool:
        query = GetUserIdByPhoneQuery(phone_number=phone_number)
        try:
            await self.__dispatcher.on_query(query)
        except KeyError:
            return False
        return True

    def __make_link(self, unique_id: str):
        webhook_url = self.__config.webhook_url.rstrip('/')
        return f"{webhook_url}/amocrm/cdr/{unique_id}.mp3"

    def __get_call_status(self, disposition: CdrDetectionEvent.Status) -> int:

        try:
            return self.__CALL_STATUSES[disposition]
        except KeyError:
            raise ValueError(f"Invalid event disposition {disposition}")

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
                f"'{caller_phone_number}' -> '{called_phone_number}'"
            )
        elif called_is_internal:
            self.__logger.info(
                "CdrDetectionEventHandler: "
                f"Unable to determine the direction of the call "
                f"for '{caller_phone_number}' -> '{called_phone_number}'"
            )

        raise Exception()

    async def __call__(self, event: CdrDetectionEvent) -> None:

        try:
            direction = await self.__get__direction(
                caller_phone_number=event.caller_phone_number,
                called_phone_number=event.called_phone_number,
            )
        except Exception:
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
            f"internal_phone_number: {internal_phone_number} "
            f"external_phone_number: {external_phone_number} ."
        )

        await asyncio.sleep(self.__config.postprocessing_delay)

        query = GetUserIdByPhoneQuery(phone_number=internal_phone_number)
        responsible_user_id = await self.__dispatcher.on_query(query)

        add_to_analytics_command = AddCallToAnalyticsCommand(
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

        try:
            await self.__dispatcher.on_command(add_to_analytics_command)
            self.__logger.debug(
                "CdrDetectionEventHandler: The call added to analytics."
            )
            return
        except Exception:
            self.__logger.debug(
                "CdrDetectionEventHandler: The call will be added to unsorted."
            )

        add_to_unsorted_command = AddCallToUnsortedCommand(
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

        try:
            await self.__dispatcher.on_command(add_to_unsorted_command)
            self.__logger.debug(
                "CdrDetectionEventHandler: The call added to unsorted."
            )
            return
        except Exception:
            self.__logger.debug(
                "CdrDetectionEventHandler: "
                "The call was not added to unsorted. "
            )

        self.__logger.error(
            "CdrDetectionEventHandler: "
            f"Failed to logging the call from event: {event} ."
        )
