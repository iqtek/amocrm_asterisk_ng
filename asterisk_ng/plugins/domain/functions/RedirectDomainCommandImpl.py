from typing import Mapping

from asterisk_ng.interfaces import CallDomainModel
from asterisk_ng.interfaces import IRedirectTelephonyCommand
from asterisk_ng.interfaces import CrmUserId
from asterisk_ng.interfaces import IRedirectDomainCommand


__all__ = ["RedirectDomainCommandImpl"]


class RedirectDomainCommandImpl(IRedirectDomainCommand):

    __slots__ = (
        "__active_calls",
        "__redirect_telephony_command",
    )

    def __init__(
        self,
        active_calls: Mapping[CrmUserId, CallDomainModel],
        redirect_telephony_command: IRedirectTelephonyCommand,
    ) -> None:
        self.__active_calls = active_calls
        self.__redirect_telephony_command = redirect_telephony_command

    async def __call__(
        self,
        user_id: CrmUserId,
        phone_number: str,
    ) -> None:
        call_model = self.__active_calls[user_id]

        await self.__redirect_telephony_command(
            phone_number=call_model.client_phone_number,
            redirect_phone_number=phone_number,
        )
