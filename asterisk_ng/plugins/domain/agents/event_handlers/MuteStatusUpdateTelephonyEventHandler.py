from typing import Mapping, MutableMapping

from asterisk_ng.interfaces import CrmUserId, CallDomainModel
from asterisk_ng.interfaces import ISendCallNotificationCommand
from asterisk_ng.interfaces import MuteStatusUpdateTelephonyEvent

from asterisk_ng.system.event_bus import IEventHandler


__all__ = ["MuteStatusUpdateTelephonyEventHandler"]


class MuteStatusUpdateTelephonyEventHandler(IEventHandler):

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

    async def __call__(self, event: MuteStatusUpdateTelephonyEvent) -> None:

        try:
            agent_id = self.__phone_to_agent_id_mapping[event.phone]
        except KeyError:
            return

        try:
            call_model: CallDomainModel = self.__active_calls[agent_id]
        except KeyError:
            return

        call_model.agent_is_mute = event.is_mute
