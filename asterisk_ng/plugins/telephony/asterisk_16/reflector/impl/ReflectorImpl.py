from asyncio import Lock

from asterisk_ng.interfaces import CallCompletedTelephonyEvent
from asterisk_ng.plugins.system.storage import IKeyValueStorage

from asterisk_ng.system.logger import ILogger

from ..core import Call, Channel
from ..core import IReflector


__all__ = ["ReflectorImpl"]


class ReflectorImpl(IReflector):

    __CHANNEL_TTL: int = 60 * 60 * 8
    __CDR_DELAY: int = 60 * 60 * 24
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

        if channel.phone is not None:
            await self.__storage.set(
                f"unique_id-channel-{channel.phone}",
                channel.unique_id,
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

    async def get_channel_by_phone(self, phone: str) -> Channel:
        unique_id = await self.__storage.get(f"unique_id-channel-{phone}")
        return await self.get_channel_by_unique_id(unique_id)

    async def update_channel_state(self, name: str, state: str) -> None:
        channel = await self.get_channel_by_name(name)
        channel.state = state.lower()
        await self.add_channel(channel)

    async def update_channel_phone(self, name: str, phone: str) -> None:
        channel = await self.get_channel_by_name(name)
        channel.phone = phone
        await self.add_channel(channel)
        await self.__logger.debug(f"Phone updated: {channel}.")

    async def delete_channel(self, channel_name: str) -> None:
        channel = await self.get_channel_by_name(channel_name)
        try:
            await self.__storage.set_expire(f"channel-unique_id-{channel.unique_id}", expire=self.__HANGUP_DELAY)
            await self.__storage.set_expire(f"unique_id-channel-{channel.name}", expire=self.__HANGUP_DELAY)
            await self.__storage.set_expire(f"linked_id-channel-{channel.name}", expire=self.__HANGUP_DELAY)
        except KeyError:
            pass  # idempotent

        if channel.phone is not None:
            await self.__storage.set_expire(f"unique_id-channel-{channel.phone}", expire=self.__HANGUP_DELAY)

        await self.__logger.debug(f"Channel deleted: {channel}.")

    async def create_call(self, linked_id: str) -> None:
        call = Call(linked_id=linked_id)
        await self.__storage.set(f"call-{linked_id}", call.json(), expire=self.__CHANNEL_TTL)
        await self.__logger.debug(f"Added new call: {call}.")

    async def get_call(self, linked_id: str) -> Call:
        json_call = await self.__storage.get(f"call-{linked_id}")
        return Call.parse_raw(json_call)

    async def add_channel_to_call(self, linked_id: str, channel_unique_id: str) -> None:
        call = await self.get_call(linked_id)
        channels_unique_ids = set(call.channels_unique_ids)
        channels_unique_ids.add(channel_unique_id)
        call.channels_unique_ids = list(channels_unique_ids)
        await self.__storage.set(f"call-{linked_id}", call.json())
        await self.__logger.debug(
            f"Added channel to call: {call} channel_unique_id: `{channel_unique_id}`."
        )

    async def delete_channel_from_call(self, linked_id: str, channel_unique_id: str) -> None:
        call = await self.get_call(linked_id)
        channels_unique_ids = set(call.channels_unique_ids)
        channels_unique_ids.discard(channel_unique_id)
        call.channels_unique_ids = list(channels_unique_ids)
        await self.__storage.set(f"call-{linked_id}", call.json())
        await self.__logger.debug(
            f"Deleted channel from call: {call} channel_unique_id: `{channel_unique_id}`."
        )

    async def delete_call(self, linked_id: str) -> None:
        await self.__storage.delete(f"call-{linked_id}")
        await self.__logger.debug(f"Call deleted: linked_id: {linked_id}.")

    async def save_call_completed_event(self, linked_id: str, event: CallCompletedTelephonyEvent) -> None:
        await self.__storage.set(f"call_completed-{linked_id}", event.json(), expire=self.__CDR_DELAY)

    async def get_call_completed_event(self, linked_id: str) -> CallCompletedTelephonyEvent:
        json_event = await self.__storage.get(f"call_completed-{linked_id}")
        return CallCompletedTelephonyEvent.parse_raw(json_event)

    async def delete_call_completed_event(self, linked_id: str) -> None:
        await self.__storage.delete(f"call_completed-{linked_id}")

    async def set_ignore_cdr_flag(self, linked_id: str) -> None:
        await self.__storage.set(f"ignore_cdr-{linked_id}", "true", expire=self.__CDR_DELAY)

    async def get_ignore_cdr_flag(self, linked_id: str) -> bool:
        try:
            await self.__storage.get(f"ignore_cdr-{linked_id}")
            return True
        except KeyError:
            return False
