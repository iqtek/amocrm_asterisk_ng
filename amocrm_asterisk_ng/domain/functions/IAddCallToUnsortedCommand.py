from glassio.dispatcher import ICommand


__all__ = [
    "IAddCallToUnsortedCommand",
]


class IAddCallToUnsortedCommand(ICommand):

    __slots__ = ()

    async def __call__(
        self,
        unique_id: str,
        caller_phone_number: str,
        called_phone_number: str,
        duration: int,
        source_name: str,
        source_uid: str,
        service_code: str,
        pipeline_name: str,
        created_at: int,
    ) -> None:
        """Add call to unsorted in pipeline."""
        raise NotImplementedError()
