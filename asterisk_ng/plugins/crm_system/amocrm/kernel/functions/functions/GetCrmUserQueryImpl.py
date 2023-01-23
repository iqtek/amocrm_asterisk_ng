from asyncio import create_task
from asyncio import sleep
from typing import MutableMapping
from typing import Optional

from amocrm_api_client import AmoCrmApiClient

from asterisk_ng.interfaces import CrmUser
from asterisk_ng.interfaces import CrmUserId
from asterisk_ng.interfaces import IGetCrmUserQuery
from asterisk_ng.system.components import AbstractInitializableComponent


__all__ = ["GetCrmUserQueryImpl"]


class GetCrmUserQueryImpl(IGetCrmUserQuery, AbstractInitializableComponent):

    __slots__ = (
        "__cache",
        "__amo_client",
        "__cache_updater",
    )

    def __init__(self, amo_client: AmoCrmApiClient) -> None:
        super().__init__(name="GetCrmUserQueryImpl")
        self.__amo_client = amo_client
        self.__cache: MutableMapping[CrmUserId, CrmUser] = {}

    async def __update_cache(self) -> None:
        while True:
            page_count = (await self.__amo_client.users.get_page()).page_count

            for page_index in range(page_count):

                page = await self.__amo_client.users.get_page(page=page_index + 1)

                for user in page.embedded:
                    user_id = CrmUserId(id=user.id, email=user.email)
                    self.__cache[user_id] = CrmUser(id=user_id, name=user.name)
            await sleep(60)

    async def _initialize(self) -> None:
        self.__cache_updater = create_task(self.__update_cache())

    async def __call__(self, user_id: CrmUserId) -> CrmUser:
        return self.__cache[user_id]

    async def _deinitialize(self, exception: Optional[Exception] = None) -> None:
        self.__cache_updater.cancel()
