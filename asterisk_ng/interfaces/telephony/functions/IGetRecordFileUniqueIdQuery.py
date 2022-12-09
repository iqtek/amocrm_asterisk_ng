from asterisk_ng.system.dispatcher import IQuery

from ..models import File


__all__ = ["IGetRecordFileByUniqueIdQuery"]


class IGetRecordFileByUniqueIdQuery(IQuery[File]):

    __slots__ = ()

    async def __call__(self, unique_id: str) -> File:
        raise NotImplementedError()
