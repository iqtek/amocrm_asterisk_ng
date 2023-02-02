from typing import Mapping
from typing import Optional
from typing import Sequence

from asterisk_ng.interfaces import Agent
from asterisk_ng.interfaces import CallReportReadyTelephonyEvent
from asterisk_ng.interfaces import CallStatus
from asterisk_ng.interfaces import CrmCallDirection
from asterisk_ng.interfaces import CrmCallResult
from asterisk_ng.interfaces import ILogCallCrmCommand

from ...functions import IGetResponsibleAgentByPhoneQuery

from asterisk_ng.system.event_bus import IEventHandler
from ...number_corrector import INumberCorrector


__all__ = ["CallReportReadyTelephonyEventHandler"]


class CallReportReadyTelephonyEventHandler(IEventHandler[CallReportReadyTelephonyEvent]):

    __STATUES_MAPPING = {
        CallStatus.ANSWERED: CrmCallResult.ANSWERED,
        CallStatus.NO_ANSWER: CrmCallResult.NO_ANSWER,
        CallStatus.BUSY: CrmCallResult.BUSY,
        CallStatus.FAILED: CrmCallResult.INVALID_NUMBER,
    }

    __slots__ = (
        "__phone_to_agent_mapping",
        "__log_call_crm_command",
        "__get_responsible_agent_by_phone_query",
        "__call_responsible_strategy",
        "__default_responsible_agent",
        "__number_corrector",
        "__last_active_agent",
    )

    def __init__(
        self,
        phone_to_agent_mapping: Mapping[str, Agent],
        log_call_crm_command: ILogCallCrmCommand,
        get_responsible_agent_by_phone_query: IGetResponsibleAgentByPhoneQuery,
        call_responsible_strategy: Sequence[str],
        default_responsible_agent: Agent,
        number_corrector: INumberCorrector,
    ) -> None:
        self.__phone_to_agent_mapping = phone_to_agent_mapping
        self.__log_call_crm_command = log_call_crm_command
        self.__get_responsible_agent_by_phone_query = get_responsible_agent_by_phone_query
        self.__call_responsible_strategy = call_responsible_strategy
        self.__default_responsible_agent = default_responsible_agent
        self.__number_corrector = number_corrector
        self.__last_active_agent: Optional[Agent] = None

    async def __get_called_agent(self, client_phone: str) -> Agent:
        agent = None

        for method in self.__call_responsible_strategy:
            if agent is not None:
                return agent

            if method == "default":
                agent = self.__default_responsible_agent
                continue

            if method == "by_entity":
                agent = await self.__get_responsible_agent_by_phone_query(client_phone)
                continue

            if method == "last_active":
                agent = self.__last_active_agent
                continue

        return self.__default_responsible_agent

    async def __call__(self, event: CallReportReadyTelephonyEvent) -> None:

        caller_agent = self.__phone_to_agent_mapping.get(event.caller_phone_number, None)
        called_agent = self.__phone_to_agent_mapping.get(event.called_phone_number, None)

        if caller_agent is None and event.called_phone_number is None:  # Incoming unanswered call.
            client_phone = self.__number_corrector.correct(event.caller_phone_number)
            called_agent = await self.__get_called_agent(client_phone)

        if caller_agent is not None and called_agent is not None:
            return  # Internal call.

        if caller_agent is None and called_agent is None:
            return  # A call without an agent.

        if caller_agent is not None:
            crm_call_direction = CrmCallDirection.OUTBOUND
            agent = caller_agent
            client_phone = event.called_phone_number
        else:  # called_agent is not None
            crm_call_direction = CrmCallDirection.INBOUND
            agent = called_agent
            client_phone = event.caller_phone_number

        self.__last_active_agent = agent

        if event.disposition != CallStatus.ANSWERED and crm_call_direction == CrmCallDirection.OUTBOUND:
            return  # Outbound and not answered calls not logging.

        call_end = event.answer_at or event.call_end_at
        duration = (event.call_end_at - call_end).seconds

        await self.__log_call_crm_command(
            unique_id=event.unique_id,
            responsible_user_id=agent.user_id,
            internal_phone_number=agent.phone,
            external_phone_number=self.__number_corrector.correct(client_phone),
            direction=crm_call_direction,
            call_result=self.__STATUES_MAPPING[event.disposition],
            duration=duration,
        )
