from typing import Mapping

from asterisk_ng.interfaces import CallReportReadyTelephonyEvent
from asterisk_ng.interfaces import CallStatus
from asterisk_ng.interfaces import CrmCallDirection
from asterisk_ng.interfaces import CrmCallResult
from asterisk_ng.interfaces import Agent
from asterisk_ng.interfaces import ILogCallCrmCommand

from asterisk_ng.system.event_bus import IEventHandler

from ...number_corrector import INumberCorrector


__all__ = ["CallCompletedEventHandler"]


class CallCompletedEventHandler(IEventHandler[CallReportReadyTelephonyEvent]):

    __STATUES_MAPPING = {
        CallStatus.ANSWERED: CrmCallResult.ANSWERED,
        CallStatus.NO_ANSWER: CrmCallResult.NO_ANSWER,
        CallStatus.BUSY: CrmCallResult.BUSY,
        CallStatus.FAILED: CrmCallResult.INVALID_NUMBER,
    }

    __slots__ = (
        "__phone_to_agent_mapping",
        "__log_call_crm_command",
        "__number_corrector",
    )

    def __init__(
        self,
        phone_to_agent_mapping: Mapping[str, Agent],
        log_call_crm_command: ILogCallCrmCommand,
        number_corrector: INumberCorrector,
    ) -> None:
        self.__phone_to_agent_mapping = phone_to_agent_mapping
        self.__log_call_crm_command = log_call_crm_command
        self.__number_corrector = number_corrector

    async def __call__(self, event: CallReportReadyTelephonyEvent) -> None:

        caller_agent = self.__phone_to_agent_mapping.get(event.caller_phone_number, None)
        called_agent = self.__phone_to_agent_mapping.get(event.called_phone_number, None)

        if caller_agent is not None and called_agent is not None:
            return  # Internal call.

        if caller_agent is None and called_agent is None:
            return  # A call without an agent.

        if caller_agent is not None:
            crm_call_direction = CrmCallDirection.OUTBOUND
            agent = caller_agent
            client_phone = event.called_phone_number

        if called_agent is not None:
            crm_call_direction = CrmCallDirection.INBOUND
            agent = called_agent
            client_phone = event.caller_phone_number

        if event.disposition != CallStatus.ANSWERED and crm_call_direction == CrmCallDirection.OUTBOUND:
            return  # Outbound and not answered calls not logging.

        duration = (event.call_end_at - event.answer_at).seconds

        await self.__log_call_crm_command(
            unique_id=event.unique_id,
            responsible_user_id=agent.user_id,
            internal_phone_number=agent.phone,
            external_phone_number=self.__number_corrector.correct(client_phone),
            direction=crm_call_direction,
            call_result=self.__STATUES_MAPPING[event.disposition],
            duration=duration,
        )
