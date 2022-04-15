from .models import File


__all__ = [
    "ITelephony",
]


class ITelephony:

    __slots__ = ()

    async def originate_call(
        self,
        caller_phone_number: str,
        called_phone_number: str,
    ) -> None:
        raise NotImplementedError()

    async def get_cdr_file_by_unique_id(self, unique_id: str) -> File:
        raise NotImplementedError()
