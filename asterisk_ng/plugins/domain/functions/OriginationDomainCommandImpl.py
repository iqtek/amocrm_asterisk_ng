from typing import Mapping

from asterisk_ng.interfaces import CrmUserId
from asterisk_ng.interfaces import IOriginationDomainCommand
from asterisk_ng.interfaces import IOriginationTelephonyCommand


__all__ = ["OriginationDomainCommandImpl"]


class OriginationDomainCommandImpl(IOriginationDomainCommand):

    __slots__ = (
        "__agent_id_to_phone_mapping",
        "__origination_telephony_command",
    )

    def __init__(
        self,
        agent_id_to_phone_mapping: Mapping[CrmUserId, str],
        origination_telephony_command: IOriginationTelephonyCommand,
    ) -> None:
        self.__agent_id_to_phone_mapping = agent_id_to_phone_mapping
        self.__origination_telephony_command = origination_telephony_command

    async def __call__(
        self,
        user_id: CrmUserId,
        phone_number: str,
    ) -> None:
        user_phone = self.__agent_id_to_phone_mapping[user_id]

        await self.__origination_telephony_command(
            caller_phone_number=user_phone,
            called_phone_number=phone_number,
        )
