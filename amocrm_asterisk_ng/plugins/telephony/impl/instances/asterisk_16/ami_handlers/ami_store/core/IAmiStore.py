__all__ = [
    "IAmiStore",
]


class IAmiStore:

    async def save_channel(
        self,
        channel: str,
        unique_id: str,
        linked_id: str,
    ) -> None:
        raise NotImplementedError()

    async def save_phone(self, channel: str, phone: str) -> None:
        raise NotImplementedError()

    async def update_phone(self, channel: str, phone: str) -> None:
        raise NotImplementedError()

    async def get_phone_by_channel(self, channel: str) -> str:
        raise NotImplementedError()

    async def get_channel_by_unique_id(self, unique_id: str) -> str:
        raise NotImplementedError()

    async def get_unique_id_by_channel(self, channel: str) -> str:
        raise NotImplementedError()

    async def get_linked_id_by_channel(self, channel: str) -> str:
        raise NotImplementedError()

    async def delete_channel(self, channel: str) -> None:
        raise NotImplementedError()

    async def set_dialbegin(self, unique_id: str, dest_unique_id: str) -> None:
        raise NotImplementedError()

    async def get_unique_id_by_dialbegin(self, unique_id: str) -> str:
        raise NotImplementedError()
