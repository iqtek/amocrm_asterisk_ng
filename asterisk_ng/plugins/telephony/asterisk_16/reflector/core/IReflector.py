from .models import Call
from .models import Channel

from asterisk_ng.interfaces import CallCompletedTelephonyEvent


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

    async def update_channel_phone(self, name: str, phone: str) -> None:
        raise NotImplementedError()

    async def delete_channel(self, channel_name: str) -> None:
        raise NotImplementedError()

    async def get_channel_by_phone(self, phone: str) -> Channel:
        raise NotImplementedError()

    async def create_call(self, linked_id: str) -> None:
        raise NotImplementedError()

    async def get_call(self, linked_id: str) -> Call:
        raise NotImplementedError()

    async def add_channel_to_call(self, linked_id: str, channel_unique_id: str) -> None:
        raise NotImplementedError()

    async def delete_channel_from_call(self, linked_id: str, channel_unique_id: str) -> None:
        raise NotImplementedError()

    async def delete_call(self, linked_id: str) -> None:
        raise NotImplementedError()

    async def save_call_completed_event(self, linked_id: str, event: CallCompletedTelephonyEvent) -> None:
        raise NotImplementedError()

    async def get_call_completed_event(self, linked_id: str) -> CallCompletedTelephonyEvent:
        raise NotImplementedError()

    async def delete_call_completed_event(self, linked_id: str) -> None:
        raise NotImplementedError()

    async def set_ignore_cdr_flag(self, linked_id: str) -> None:
        raise NotImplementedError()

    async def get_ignore_cdr_flag(self, linked_id: str) -> bool:
        raise NotImplementedError()
