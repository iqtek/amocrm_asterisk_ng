from datetime import datetime
from time import time

from glassio.context import get_context
from amocrm_asterisk_ng.domain import CallCompletedEvent
from amocrm_asterisk_ng.domain import CallStatus
from glassio.logger import ILogger
from glassio.event_bus import IEventBus

from ..ami_store import IAmiStore
from ......core.ami_manager import Event
from ......core.ami_manager import IAmiEventHandler


__all__ = [
    "CdrEventHandler",
]


class CdrEventHandler(IAmiEventHandler):

    __slots__ = (
        "__event_bus",
        "__ami_store",
        "__logger",
    )

    __DATETIME_MASK = "%Y-%m-%d %H:%M:%S"

    __DISPOSITION_MAPPING = {
        "CANCEL": CallStatus.CANCEL,
        "ANSWERED": CallStatus.ANSWER,
        "NO ANSWER": CallStatus.NO_ANSWER,
        "BUSY": CallStatus.BUSY,
        "CONGESTION": CallStatus.CONGESTION,
        "CHANUNAVAIL": CallStatus.CHANUNAVAIL,
    }

    def __init__(
        self,
        event_bus: IEventBus,
        ami_store: IAmiStore,
        logger: ILogger,
    ) -> None:
        self.__ami_store = ami_store
        self.__event_bus = event_bus
        self.__logger = logger

    @classmethod
    def event_pattern(cls) -> str:
        return "Cdr"

    def __convert_datetime(self, str_datetime) -> datetime:
        return datetime.strptime(
            str_datetime,
            self.__DATETIME_MASK
        )

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

        channel_unique_id = await self.__ami_store.get_unique_id_by_channel(
            channel=channel,
        )

        destination_channel_linked_id = await self.__ami_store.get_linked_id_by_channel(
            channel=destination_channel,
        )

        # Reject symmetrical CDR.
        if destination_channel_linked_id != channel_unique_id:
            await self.__logger.debug(
                "CdrEventHandler: "
                "Symmetric CDR detected. "
                f"destination_channel_linked_id: "
                f"'{destination_channel_linked_id}' "
                f"channel_unique_id: "
                f"'{channel_unique_id} ."
            )
            return

        if "Local/" in channel:
            at_index = channel.find('@')
            caller_phone_number = channel[6:at_index]
        else:
            caller_phone_number = await self.__ami_store.get_phone_by_channel(
                channel=channel,
            )

        if "Local/" in destination_channel:
            at_index = destination_channel.find('@')
            called_phone_number = destination_channel[6:at_index]
        else:
            called_phone_number = await self.__ami_store.get_phone_by_channel(
                channel=destination_channel,
            )

        start_time = self.__convert_datetime(str_start_time)
        end_time = self.__convert_datetime(str_end_time)

        str_answer_time = event.get("AnswerTime", default=None)
        if str_answer_time:
            answer_time = self.__convert_datetime(str_answer_time)
        else:
            answer_time = None

        disposition = self.__get_disposition(str_disposition)

        answer_timestamp = None

        if answer_time is not None:
            answer_timestamp = answer_time.timestamp()

        cdr_event = CallCompletedEvent(
            unique_id=unique_id,
            created_at=time(),
            caller_phone_number=caller_phone_number,
            called_phone_number=called_phone_number,
            duration=duration,
            disposition=disposition,
            start_timestamp=start_time.timestamp(),
            end_timestamp=end_time.timestamp(),
            answer_timestamp=answer_timestamp,
        )
        await self.__event_bus.publish(cdr_event)
