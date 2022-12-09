from typing import Mapping

from asterisk_ng.interfaces import CrmUserId
from asterisk_ng.interfaces import ISetMuteDomainCommand
from asterisk_ng.interfaces import ISetMuteTelephonyCommand


__all__ = ["SetMuteDomainCommandImpl"]


class SetMuteDomainCommandImpl(ISetMuteDomainCommand):

    __slots__ = (
        "__agent_id_to_phone_mapping",
        "__set_mute_telephony_command",
    )

    def __init__(
        self,
        agent_id_to_phone_mapping: Mapping[CrmUserId, str],
        set_mute_telephony_command: ISetMuteTelephonyCommand,
    ) -> None:
        self.__agent_id_to_phone_mapping = agent_id_to_phone_mapping
        self.__set_mute_telephony_command = set_mute_telephony_command

    async def __call__(
        self,
        user_id: CrmUserId,
        is_mute: bool,
    ) -> None:
        user_phone = self.__agent_id_to_phone_mapping[user_id]

        await self.__set_mute_telephony_command(
            phone_number=user_phone,
            is_mute=is_mute,
        )
