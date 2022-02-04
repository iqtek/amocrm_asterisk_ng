from asterisk_amocrm.infrastructure.dispatcher import IQuery
from asterisk_amocrm.domains.models import Filetype


__all__ = [
    "GetCdrByUniqueIdQuery"
]


class GetCdrByUniqueIdQuery(IQuery):
    unique_id: str
    file_type: Filetype
