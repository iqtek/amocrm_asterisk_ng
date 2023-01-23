from typing import Mapping
from typing import MutableMapping

from asterisk_ng.interfaces import Agent
from asterisk_ng.interfaces import CallCompletedTelephonyEvent
from asterisk_ng.interfaces import CallDomainModel
from asterisk_ng.interfaces import CrmUserId

from asterisk_ng.system.event_bus import IEventHandler


__all__ = ["CallCompletedTelephonyEventHandler"]


class CallCompletedTelephonyEventHandler(IEventHandler):

    __slots__ = (
        "__active_calls",
        "__phone_to_agent_mapping",
    )

    def __init__(
        self,
        active_calls: MutableMapping[CrmUserId, CallDomainModel],
        phone_to_agent_mapping: Mapping[str, Agent],
    ) -> None:
        self.__active_calls = active_calls
        self.__phone_to_agent_mapping = phone_to_agent_mapping

    async def __call__(self, event: CallCompletedTelephonyEvent) -> None:

        if agent := self.__phone_to_agent_mapping.get(event.caller_phone_number, None):
            self.__active_calls.pop(agent.user_id, None)

        if agent := self.__phone_to_agent_mapping.get(event.called_phone_number, None):
            self.__active_calls.pop(agent.user_id, None)
