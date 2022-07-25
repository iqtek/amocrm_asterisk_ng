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
        """
        Get cdr file by unique_id.

        :param unique_id: CDR unique_id.
        :type unique_id: str
        :return: Audio file.
        :rtype: File
        """
        raise NotImplementedError()
