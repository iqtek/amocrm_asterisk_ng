from datetime import datetime

from asterisk_ng.interfaces import CallCompletedTelephonyEvent
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
        channel = event["Channel"]
        destination_channel = event["DestinationChannel"]
        unique_id = event["Uniqueid"]
        duration = int(event["Duration"])
        str_disposition = event["Disposition"]
        str_start_time = event["StartTime"]
        str_end_time = event["EndTime"]

        caller_phone_number = await self.__reflector.get_phone(channel)
        called_phone_number = await self.__reflector.get_phone(destination_channel)

        if ';2' in channel:
            return  # Reject symmetrical CDR.

        start_datetime = self.__convert_datetime(str_start_time)
        end__datetime = self.__convert_datetime(str_end_time)

        if str_answer_time := event.get("AnswerTime", None):
            answer_datetime = self.__convert_datetime(str_answer_time)
        else:
            answer_datetime = None

        disposition = self.__get_disposition(str_disposition)

        call_completed_event = CallCompletedTelephonyEvent(
            unique_id=unique_id,
            created_at=datetime.now(),
            caller_phone_number=caller_phone_number,
            called_phone_number=called_phone_number,
            duration=duration,
            disposition=disposition,
            call_start_at=start_datetime,
            call_end_at=end__datetime,
            answer_at=answer_datetime,
        )

        await self.__event_bus.publish(call_completed_event)
