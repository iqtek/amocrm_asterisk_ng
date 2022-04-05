from asterisk_amocrm.domains.models import File
from asterisk_amocrm.domains.models import Filetype
from asterisk_amocrm.infrastructure import IQuery


__all__ = [
    "IGetCdrByUniqueIdQuery",
]


class IGetCdrByUniqueIdQuery(IQuery):

    async def __call__(
        self,
        unique_id: str,
    ) -> File:
        """
        Get cdr file .mp3 by his unique_id.
        :raise FileNotFoundError: If the file does not exist.
        """
        raise NotImplementedError()
