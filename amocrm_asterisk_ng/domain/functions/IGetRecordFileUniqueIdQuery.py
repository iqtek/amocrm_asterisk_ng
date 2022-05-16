from glassio.dispatcher import IQuery

from ..models import File


__all__ = [
    "IGetRecordFileUniqueIdQuery",
]


class IGetRecordFileUniqueIdQuery(IQuery[File]):

    __slots__ = ()

    async def __call__(
        self,
        unique_id: str,
    ) -> File:
        raise NotImplementedError()
