from typing import MutableMapping
from typing import Mapping

from asterisk_ng.interfaces import CallCompletedTelephonyEvent
from asterisk_ng.interfaces import CallDomainModel
from asterisk_ng.interfaces import CrmUserId

from asterisk_ng.system.event_bus import IEventHandler
from asterisk_ng.system.logger import ILogger


__all__ = ["CallCompletedTelephonyEventHandler"]


class CallCompletedTelephonyEventHandler(IEventHandler):

    __slots__ = (
        "__active_calls",
        "__phone_to_agent_id_mapping",
    )

    def __init__(
        self,
        active_calls: MutableMapping[CrmUserId, CallDomainModel],
        phone_to_agent_id_mapping: Mapping[str, CrmUserId],
    ) -> None:
        self.__active_calls = active_calls
        self.__phone_to_agent_id_mapping = phone_to_agent_id_mapping

    async def __call__(self, event: CallCompletedTelephonyEvent) -> None:

        if agent_id := self.__phone_to_agent_id_mapping.get(event.caller_phone_number, None):
            self.__active_calls.pop(agent_id, None)

        if agent_id := self.__phone_to_agent_id_mapping.get(event.called_phone_number, None):
            self.__active_calls.pop(agent_id, None)
