from asterisk_amocrm.domains.models import File
from asterisk_amocrm.infrastructure.dispatcher import IQueryHandler
from ..queries import GetCdrByUniqueIdQuery

__all__ = [
    "IGetCdrByUniqueIdQH",
]


class IGetCdrByUniqueIdQH(IQueryHandler):

    async def __call__(self, query: GetCdrByUniqueIdQuery) -> File:
        """
        Get cdr file .mp3 by his unique_id.
        :raise FileNotFoundError: If the file does not exist.
        """
        raise NotImplementedError()
