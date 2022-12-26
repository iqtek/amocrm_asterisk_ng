from .models import Channel
from typing import Collection
from typing import Tuple

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

    async def add_to_call(
        self,
        linked_id: str,
        phone: str
    ) -> None:
        raise NotImplementedError()

    async def delete_call(self, linked_id: str) -> None:
        raise NotImplementedError()


    async def get_call_phones(self, linked_id: str) -> Collection[str]:
        raise NotImplementedError()
