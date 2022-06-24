from amocrm_asterisk_ng.infrastructure import IKeyValueStorage
from glassio.logger import ILogger

from ..core import IAmiStore


__all__ = [
    "AmiStoreImpl",
]


class AmiStoreImpl(IAmiStore):

    __CHANNEL_TTL: int = 60 * 60 * 8
    __DIAL_WAITING_TIME = 2

    def __init__(
        self,
        storage: IKeyValueStorage,
        logger: ILogger,
    ) -> None:
        self.__storage = storage
        self.__logger = logger

    async def save_channel(
        self,
        channel: str,
        unique_id: str,
        linked_id: str,
    ) -> None:

        await self.__storage.set(
            f"channel-unique_id-{unique_id}",
            channel,
            expire=self.__CHANNEL_TTL
        )
        await self.__storage.set(
            f"unique_id-channel-{channel}",
            unique_id,
            expire=self.__CHANNEL_TTL
        )
        await self.__storage.set(
            f"linked_id-channel-{channel}",
            linked_id,
            expire=self.__CHANNEL_TTL
        )

        await self.__logger.debug(
            "AmiStore: create new channel "
            f"[ channel: '{channel}' "
            f"unique_id: '{unique_id}' "
            f"linked_id: '{linked_id}' ]."
        )

    async def save_phone(self, channel: str, phone: str) -> None:
        await self.__storage.set(
            f"phone-channel-{channel}",
            phone,
            expire=self.__CHANNEL_TTL
        )

        await self.__logger.debug(
            "AmiStore: save phone "
            f"[ channel: '{channel}' "
            f"phone: '{phone}' ]."
        )

    async def update_phone(self, channel: str, phone: str) -> None:
        old_phone = await self.get_phone_by_channel(channel)
        await self.__storage.update(
            f"phone-channel-{channel}",
            phone,
            expire=self.__CHANNEL_TTL
        )

        await self.__logger.debug(
            "AmiStore: update phone "
            f"[ channel: '{channel}' "
            f"old_phone: '{old_phone}' "
            f"new_phone: '{phone}' ]."
        )

    async def get_phone_by_channel(self, channel: str) -> str:
        return await self.__storage.get(
            f"phone-channel-{channel}",
        )

    async def get_channel_by_unique_id(self, unique_id: str) -> str:
        return await self.__storage.get(
            f"channel-unique_id-{unique_id}",
        )

    async def get_unique_id_by_channel(self, channel: str) -> str:
        return await self.__storage.get(
            f"unique_id-channel-{channel}",
        )

    async def get_linked_id_by_channel(self, channel: str) -> str:
        return await self.__storage.get(
            f"linked_id-channel-{channel}",
        )

    async def delete_channel(self, channel: str) -> None:

        unique_id = await self.get_unique_id_by_channel(channel)

        await self.__storage.delete(
            f"channel-unique_id-{unique_id}",
        )
        await self.__storage.delete(
            f"unique_id-channel-{channel}",
        )
        await self.__storage.delete(
            f"linked_id-channel-{channel}",
        )
        await self.__storage.delete(
            f"phone-channel-{channel}",
        )

        await self.__logger.debug(
            "AmiStore: delete channel "
            f"[ channel: '{channel}' "
            f"unique_id: '{unique_id}' ]."
        )

    async def set_dialbegin(self, unique_id: str, dest_unique_id: str) -> None:
        await self.__storage.set(
            f"dialbegin-{dest_unique_id}",
            unique_id,
            expire=self.__DIAL_WAITING_TIME,
        )

        await self.__logger.debug(
            "AmiStore: set dialbegin "
            f"[ unique_id: '{unique_id}' "
            f"dest_unique_id: '{dest_unique_id}' ]."
        )

    async def get_unique_id_by_dialbegin(self, unique_id: str) -> str:
        return await self.__storage.get(
            f"dialbegin-{unique_id}",
        )
