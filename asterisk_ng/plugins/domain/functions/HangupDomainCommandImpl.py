from typing import Mapping

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
        hangup_telephony_command: IHangupTelephonyCommand,
    ) -> None:
        self.__agent_id_to_phone_mapping = agent_id_to_phone_mapping
        self.__hangup_telephony_command = hangup_telephony_command

    async def __call__(self, user_id: CrmUserId) -> None:
        agent_phone = self.__agent_id_to_phone_mapping[user_id]
        await self.__hangup_telephony_command(phone_number=agent_phone)
