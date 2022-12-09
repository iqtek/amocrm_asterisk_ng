from .models import Channel
from typing import Collection


__all__ = [
    "IReflector",
]


class IReflector:

    __slots__ = ()

    async def add_channel(self, channel: Channel) -> None:
        raise NotImplementedError()

    async def get_channel_by_name(self, name: str) -> Channel:
        raise NotImplementedError()

    async def get_channel_by_unique_id(self, unique_id: str) -> Channel:
        raise NotImplementedError()

    async def update_channel_state(self, name: str, state: str) -> None:
        raise NotImplementedError()

    async def delete_channel(self, channel_name: str) -> None:
        raise NotImplementedError()

    async def attach_phone(self, channel_name: str, phone: str) -> None:
        raise NotImplementedError()

    async def get_phone(self, channel_name: str) -> str:
        raise NotImplementedError()

    async def get_channel_by_phone(self, phone: str) -> Channel:
        raise NotImplementedError()

    async def add_bridge(self, unique_id: str) -> None:
        raise NotImplementedError()

    async def delete_bridge(self, unique_id: str) -> None:
        raise NotImplementedError()

    async def get_channels_in_bridge(self, unique_id: str) -> Collection[str]:
        raise NotImplementedError()

    async def bridge_enter_channel(
        self,
        bridge_unique_id: str,
        channel_name,
    ) -> None:
        raise NotImplementedError()

    async def bridge_leave_channel(
        self,
        bridge_unique_id: str,
        channel_name,
    ) -> None:
        raise NotImplementedError()
