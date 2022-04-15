from amocrm_asterisk_ng.infrastructure import ICommand


__all__ = [
    "IAddCallToUnsortedCommand",
]


class IAddCallToUnsortedCommand(ICommand):

    __slots__ = ()

    async def __call__(
        self,
        source_name: str,
        source_uid: str,
        pipeline_id: int,
        created_at: int,
        uniq: str,
        duration: int,
        service_code: str,
        link: str,
        called: str,
        caller: str,
       ) -> None:
        raise NotImplementedError()
