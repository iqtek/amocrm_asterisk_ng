from typing import Collection

from asterisk_ng.system.dispatcher import ICommand

from ..models import CrmUserId


__all__ = ["ISendCallNotificationCommand"]


class ISendCallNotificationCommand(ICommand):

    __slots__ = ()

    async def __call__(
        self,
        phone_number: str,
        users: Collection[CrmUserId],
    ) -> None:
        raise NotImplementedError()
