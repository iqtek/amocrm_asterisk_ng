from typing import Mapping

from asterisk_ng.interfaces import CallCompletedTelephonyEvent
from asterisk_ng.interfaces import CallStatus
from asterisk_ng.interfaces import CrmCallDirection
from asterisk_ng.interfaces import CrmCallResult
from asterisk_ng.interfaces import CrmUserId
from asterisk_ng.interfaces import ILogCallCrmCommand

from asterisk_ng.system.event_bus import IEventHandler


__all__ = ["CallCompletedEventHandler"]


class CallCompletedEventHandler(IEventHandler[CallCompletedTelephonyEvent]):

    __STATUES_MAPPING = {
        CallStatus.ANSWERED: CrmCallResult.ANSWERED,
        CallStatus.NO_ANSWER: CrmCallResult.NO_ANSWER,
        CallStatus.BUSY: CrmCallResult.BUSY,
        CallStatus.FAILED: CrmCallResult.INVALID_NUMBER,
    }

    __slots__ = (
        "__phone_to_agent_id_mapping",
        "__log_call_crm_command",
    )

    def __init__(
        self,
        phone_to_agent_id_mapping: Mapping[str, CrmUserId],
        log_call_crm_command: ILogCallCrmCommand,
    ) -> None:
        self.__phone_to_agent_id_mapping = phone_to_agent_id_mapping
        self.__log_call_crm_command = log_call_crm_command

    async def __call__(self, event: CallCompletedTelephonyEvent) -> None:

        caller_agent_id = self.__phone_to_agent_id_mapping.get(event.caller_phone_number, None)
        called_agent_id = self.__phone_to_agent_id_mapping.get(event.called_phone_number, None)

        if caller_agent_id is not None and called_agent_id is not None:
            return  # Internal call.

        if caller_agent_id is None and called_agent_id is None:
            return  # A call without an agent.

        agent_id = caller_agent_id or called_agent_id
        crm_call_direction = CrmCallDirection.INBOUND if caller_agent_id is None else CrmCallDirection.OUTBOUND

        if event.disposition != CallStatus.ANSWERED and crm_call_direction == CrmCallDirection.OUTBOUND:
            return  # Outbound and not answered calls not logging.

        phone_number = event.caller_phone_number if crm_call_direction == CrmCallDirection.INBOUND else event.called_phone_number
        phone_number2 = event.called_phone_number if crm_call_direction == CrmCallDirection.INBOUND else event.caller_phone_number

        duration = (event.call_end_at - event.answer_at).seconds

        await self.__log_call_crm_command(
            unique_id=event.unique_id,
            responsible_user_id=agent_id,
            phone_number=phone_number,
            phone_number2=phone_number2,
            direction=crm_call_direction,
            call_result=self.__STATUES_MAPPING[event.disposition],
            duration=duration,
        )
