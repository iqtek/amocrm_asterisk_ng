from asterisk_amocrm.domains import File


__all__ = [
    "ITelephony",
]


class ITelephony:

    __slots__ = ()

    async def originate_call(self) -> None:
        raise NotImplementedError()

    async def get_cdr_by_unique_id(self) -> File:
        raise NotImplementedError()
