from datetime import datetime
from typing import MutableMapping
from typing import MutableSequence
from asyncio import sleep, create_task

from collections import defaultdict
from asterisk_ng.interfaces import CallReportReadyTelephonyEvent
from asterisk_ng.interfaces import CallStatus

from asterisk_ng.plugins.telephony.ami_manager import Event
from asterisk_ng.plugins.telephony.ami_manager import IAmiEventHandler

from asterisk_ng.system.event_bus import IEventBus
from asterisk_ng.system.logger import ILogger

from ...core import IReflector


__all__ = ["CdrEventHandler"]


class CdrEventHandler(IAmiEventHandler):

    __DISPOSITION_MAPPING = {
        "FAILED": CallStatus.FAILED,
        "ANSWERED": CallStatus.ANSWERED,
        "NO ANSWER": CallStatus.NO_ANSWER,
        "BUSY": CallStatus.BUSY,
        "CONGESTION": CallStatus.FAILED,
    }

    __slots__ = (
        "__reflector",
        "__event_bus",
        "__logger",
        "__event_buffer",
    )

    def __init__(
        self,
        reflector: IReflector,
        event_bus: IEventBus,
        logger: ILogger,
    ) -> None:
        self.__reflector = reflector
        self.__event_bus = event_bus
        self.__logger = logger

    def __convert_datetime(self, str_datetime) -> datetime:
        return datetime.strptime(str_datetime, "%Y-%m-%d %H:%M:%S")

    def __get_disposition(
        self,
        str_disposition: str
    ) -> CallStatus:
        try:
            return self.__DISPOSITION_MAPPING[str_disposition]
        except KeyError:
            raise ValueError(f"Unknown disposition {str_disposition}.")

    async def __call__(self, event: Event) -> None:
        create_task(self.call2(event))

    async def call2(self, event: Event) -> None:

        await sleep(3.0)

        cdr_linkedid = event["linkedid"]

        if await self.__reflector.get_ignore_cdr_flag(cdr_linkedid):
            return

        try:
            call_completed_event = await self.__reflector.get_call_completed_event(cdr_linkedid)
        except KeyError:
            await self.__logger.info("Saved CallCompletedEvent not found.")
        else:
            caller_phone_number = call_completed_event.caller_phone_number
            called_phone_number = call_completed_event.called_phone_number

        unique_id = event["Uniqueid"]
        duration = int(event["Duration"])
        str_disposition = event["Disposition"]
        str_start_time = event["StartTime"]
        str_end_time = event["EndTime"]

        start_datetime = self.__convert_datetime(str_start_time)
        end_datetime = self.__convert_datetime(str_end_time)

        if str_answer_time := event.get("AnswerTime", None):
            answer_datetime = self.__convert_datetime(str_answer_time)
        else:
            answer_datetime = None

        disposition = self.__get_disposition(str_disposition)

        if call_completed_event.disposition == CallStatus.ANSWERED and disposition != CallStatus.ANSWERED:
            return

        if call_completed_event.disposition != CallStatus.ANSWERED and disposition == CallStatus.ANSWERED:
            return

        call_report_ready_telephony_event = CallReportReadyTelephonyEvent(
            unique_id=unique_id,
            created_at=datetime.now(),
            caller_phone_number=caller_phone_number,
            called_phone_number=called_phone_number,
            duration=duration,
            disposition=disposition,
            call_start_at=start_datetime,
            call_end_at=end_datetime,
            answer_at=answer_datetime,
        )

        await self.__event_bus.publish(call_report_ready_telephony_event)
        await self.__reflector.set_ignore_cdr_flag(cdr_linkedid)

        if called_phone_number is not None:
            await self.__reflector.delete_call_completed_event(cdr_linkedid)
