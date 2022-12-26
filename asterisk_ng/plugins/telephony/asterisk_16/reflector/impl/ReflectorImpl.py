from asyncio import Lock
import json
from typing import Collection

from asterisk_ng.plugins.system.storage import IKeyValueStorage
from asterisk_ng.system.logger import ILogger

from ..core import Channel
from ..core import IReflector


__all__ = ["ReflectorImpl"]


class ReflectorImpl(IReflector):

    __CHANNEL_TTL: int = 60 * 60 * 8
    __HANGUP_DELAY: int = 60 * 60
    
    def __init__(
        self,
        storage: IKeyValueStorage,
        logger: ILogger,
    ) -> None:
        self.__storage = storage
        self.__logger = logger

        self.__lock = Lock()

    async def add_channel(self, channel: Channel) -> None:

        await self.__storage.set(
            f"channel-unique_id-{channel.unique_id}",
            channel.json(),
            expire=self.__CHANNEL_TTL
        )

        await self.__storage.set(
            f"unique_id-channel-{channel.name}",
            channel.unique_id,
            expire=self.__CHANNEL_TTL
        )
        await self.__storage.set(
            f"linked_id-channel-{channel.name}",
            channel.linked_id,
            expire=self.__CHANNEL_TTL
        )

        await self.__logger.debug(f"Added new channel: {channel}.")

    async def get_channel_by_name(self, name: str) -> Channel:
        unique_id = await self.__storage.get(f"unique_id-channel-{name}")
        json_channel = await self.__storage.get(f"channel-unique_id-{unique_id}")
        return Channel.parse_raw(json_channel)

    async def get_channel_by_unique_id(self, unique_id: str) -> Channel:
        json_channel = await self.__storage.get(f"channel-unique_id-{unique_id}")
        return Channel.parse_raw(json_channel)

    async def update_channel_state(self, name: str, state: str) -> None:
        channel = await self.get_channel_by_name(name)
        channel.state = state
        await self.add_channel(channel)

    async def delete_channel(self, channel_name: str) -> None:
        channel = await self.get_channel_by_name(channel_name)

        await self.__storage.set_expire(f"channel-unique_id-{channel.unique_id}", expire=self.__HANGUP_DELAY)
        await self.__storage.set_expire(f"unique_id-channel-{channel.name}", expire=self.__HANGUP_DELAY)
        await self.__storage.set_expire(f"linked_id-channel-{channel.name}", expire=self.__HANGUP_DELAY)

        try:
            phone = await self.get_phone(channel_name)
        except KeyError:
            pass
        else:
            await self.__storage.set_expire(f"phone-channel-{channel_name}", expire=self.__HANGUP_DELAY)
            await self.__storage.set_expire(f"channel-phone-{phone}", expire=self.__HANGUP_DELAY)

        await self.__logger.debug(f"Channel deleted: {channel}.")

    async def attach_phone(self, channel_name: str, phone: str) -> None:

        try:
            await self.get_phone(channel_name=channel_name)
        except KeyError:
            pass
        else:
            return

        await self.__storage.set(
            f"phone-channel-{channel_name}",
            phone,
            expire=self.__CHANNEL_TTL
        )

        await self.__storage.set(
            f"channel-phone-{phone}",
            channel_name,
            expire=self.__CHANNEL_TTL
        )

        await self.__logger.debug(
            f"Phone associated ({phone} -> {channel_name})."
        )

    async def get_phone(self, channel_name: str) -> str:
        return await self.__storage.get(f"phone-channel-{channel_name}")

    async def get_channel_by_phone(self, phone: str) -> Channel:
        channel_name = await self.__storage.get(f"channel-phone-{phone}")
        return await self.get_channel_by_name(channel_name)

    async def add_to_call(
        self,
        linked_id: str,
        phone: str
    ) -> None:
        try:
            phones = set(json.loads(await self.__storage.get(f"call-{linked_id}")))
        except KeyError:
            phones = set()
        phones.add(phone)
        phones_str = json.dumps(list(phones))
        await self.__storage.set(f"call-{linked_id}", phones_str)

    async def delete_call(self, linked_id: str) -> None:
        await self.__storage.delete(f"call-{linked_id}")

    async def get_call_phones(self, linked_id: str) -> Collection[str]:
        phones_str = await self.__storage.get(f"call-{linked_id}")
        return json.loads(phones_str)
