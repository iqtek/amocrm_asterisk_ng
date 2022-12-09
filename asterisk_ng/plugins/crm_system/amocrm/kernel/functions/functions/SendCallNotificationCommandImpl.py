from typing import Collection

from amocrm_api_client import AmoCrmApiClient

from asterisk_ng.interfaces import CrmUserId
from asterisk_ng.interfaces import ISendCallNotificationCommand


__all__ = ["SendCallNotificationCommandImpl"]


class SendCallNotificationCommandImpl(ISendCallNotificationCommand):

    __slots__ = (
        "__amo_client",
    )

    def __init__(self, amo_client: AmoCrmApiClient) -> None:
        self.__amo_client = amo_client

    async def __call__(
        self,
        phone_number: str,
        users: Collection[CrmUserId],
    ) -> None:
        await self.__amo_client.events.add_card(
            phone_number=phone_number,
            users=[user.id for user in users],
        )
