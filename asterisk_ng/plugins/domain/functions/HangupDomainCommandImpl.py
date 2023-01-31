from typing import Mapping
from typing import MutableMapping

from asterisk_ng.interfaces import CallDomainModel
from asterisk_ng.interfaces import CrmUserId
from asterisk_ng.interfaces import IHangupDomainCommand
from asterisk_ng.interfaces import IHangupTelephonyCommand


__all__ = ["HangupDomainCommandImpl"]


class HangupDomainCommandImpl(IHangupDomainCommand):

    __slots__ = (
        "__agent_id_to_phone_mapping",
        "__hangup_telephony_command"
    )

    def __init__(
        self,
        agent_id_to_phone_mapping: Mapping[CrmUserId, str],
        active_calls: MutableMapping[CrmUserId, CallDomainModel],
        hangup_telephony_command: IHangupTelephonyCommand,
    ) -> None:
        self.__agent_id_to_phone_mapping = agent_id_to_phone_mapping
        self.__active_calls = active_calls
        self.__hangup_telephony_command = hangup_telephony_command

    async def __call__(self, user_id: CrmUserId) -> None:
        agent_phone = self.__agent_id_to_phone_mapping[user_id]
        self.__active_calls.pop(user_id, None)
        await self.__hangup_telephony_command(phone_number=agent_phone)
