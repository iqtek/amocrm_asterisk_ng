from typing import Collection
from .CallStatus import CallStatus


class ICrm:

    __slots__ = ()

    async def is_user_phone_number(self, phone_number: str) -> bool:
        raise NotImplementedError()

    async def get_user_id_by_phone(self, phone_number: str) -> int:
        raise NotImplementedError()

    async def raise_card(self, phone_number: str, users: Collection[int]) -> None:
        raise NotImplementedError()

    async def get_pipeline_id_py_name(self, pipeline_name: str) -> int:
        raise NotImplementedError()

    async def add_call_to_analytics(
        self,
        unique_id: str,
        phone_number: str,
        direction: Literal["inbound", "outbound"],
        duration: int,
        source: str,
        created_at: int,
        responsible_user_id: int,
        call_status: CallStatus,
    ) -> None:
        raise NotImplementedError()

    async def add_call_to_unsorted(
        self,
        unique_id: str,
        caller_phone_number: str,
        called_phone_number: str,
        duration: int,
        source_name: str,
        source_uid: str,
        service_code: str,
        pipeline_id: int,
        created_at: int,
    ) -> None:
        raise NotImplementedError()
